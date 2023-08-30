import sys

import anyio
from google.cloud import run_v2
import os
import dagger

PROJECT = 'prod-datascience-393718'
GCR_SERVICE_URL = f"projects/{PROJECT}/locations/us-central1/services/querycraftergg"
GCR_PUBLISH_ADDRESS = f"gcr.io/{PROJECT}/querycrafter"

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


async def main():
    version = '3.10'

    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        app = client.host().directory(root)  # Asegúrate de cambiar esto a la ruta real de tu código

        python_container = (
            client.container(platform=dagger.Platform("linux/amd64")).from_(f"python:{version}-slim-buster"))
        container = (
            python_container.with_directory("/app", app)
            .with_workdir("/app")
            .with_exec(["pip", "install", "poetry"])
            .with_exec(["poetry", "config", "virtualenvs.create", "false"])
            .with_exec(["poetry", "install", "--no-interaction", "--no-ansi"])
            .with_exec(["pytest"])
            .with_exposed_port(8080)
            .with_entrypoint(["python", "-m", "app"])
        )

        # publish the container to GCR object
        container_image = await container.publish(GCR_PUBLISH_ADDRESS)
        print(f"Container published to {container_image}.")

        gcr_client = run_v2.ServicesClient()

        # define a service request
        gcr_request = run_v2.UpdateServiceRequest(
            service=run_v2.Service(
                name=GCR_SERVICE_URL,
                template=run_v2.RevisionTemplate(
                    containers=[
                        run_v2.Container(
                            image=container_image,
                            ports=[
                                run_v2.ContainerPort(
                                    name="http1",
                                    container_port=8080,
                                ),
                            ],
                            startup_probe=run_v2.Probe(  # Agregando el health check aquí
                                initial_delay_seconds=30,
                                period_seconds=5,
                                http_get=run_v2.HTTPGetAction(
                                    path="/healthcheck",
                                    port=8080
                                )
                            ),
                        ),
                    ],
                ),
            )
        )
        # update service
        gcr_operation = gcr_client.update_service(request=gcr_request)
        print("GCP service update request sent.")

        # wait for service request completion
        response = gcr_operation.result()
        print("GCP service update request completed.")

    print(f"Deployment for image {container_image} now available at {response}.")


anyio.run(main)

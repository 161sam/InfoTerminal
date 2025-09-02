# NiFi Aleph Ingestion Flow

This directory contains a NiFi template for ingesting files from a watch folder and sending them to Aleph.

## Usage

1. Copy `params/aleph_ingest.env.example` to your environment and adjust values.
2. Import `templates/aleph_ingest_watchfolder.xml` into NiFi using the deploy script:
   ```bash
   bash etl/nifi/scripts/deploy_aleph_ingest.sh
   ```
3. In the NiFi UI, create a Parameter Context using variables from the example file and bind it to the instantiated process group.
4. Enable controller services such as `DetectContent` for MIME detection.
5. Start processors in order: controller services, then processors.
6. Successful uploads are moved to `${NIFI_SUCCESS_DIR}`, failures to `${NIFI_FAILURE_DIR}` for DLQ handling.
7. Monitor bulletins for errors. Retrys are handled by NiFi; unresolved failures land in the failure directory.

## Security

API keys should be provided via Kubernetes Secrets or ExternalSecret integrations.

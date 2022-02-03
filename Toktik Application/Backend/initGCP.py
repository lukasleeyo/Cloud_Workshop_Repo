class InitGCP:
    def initDB():
        from google.cloud import firestore

        # Explicitly use service account credentials by specifying the private key
        # file.
        firestore_client = firestore.Client.from_service_account_json(
            # CREDENTIALS
        )

        return firestore_client

    def initStorage():
        from google.cloud import storage

        # Explicitly use service account credentials by specifying the private key
        # file.
        storage_client = storage.Client.from_service_account_json(
            # CREDENTIALS
        )

        # # Make an authenticated API request
        # buckets = list(storage_client.list_buckets())
        # print(buckets)
        return storage_client

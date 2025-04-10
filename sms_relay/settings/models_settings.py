class ModelSettings:
    @property
    def project_models(self):
       return [
           "database.models.sms_forwarding.message",
       ]

    @property
    def model_registry(self):
        return [
            "aerich.models",
            *self.project_models,
        ]
    


class ReportsService:
    def __init__(self, reports_repository):
        self.reports_repository = reports_repository

    def list_reports(self):
        return self.reports_repository.list_all()

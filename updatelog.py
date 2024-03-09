import json
class UpdateLog:
    def __init__(self):
        self.filename = "./update/update.json"

    def get_update_log(self):
        last_log = {}
        with open(self.filename, "r", encoding="utf-8") as file:
            log = json.load(file)  
            last_update = log["update_list"][-1]
            last_log["content"] = last_update["content"]
            last_log["date"] = last_update["update_date"]
            last_log["ver"] = last_update["ver"]
        return last_log
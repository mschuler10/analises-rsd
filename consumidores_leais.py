import statistics
from databaseDAO import DatabaseDAO

class LoyalConsumers:
    def __init__(self):
        self.db_host = "your_db_host"
        self.db_name = "your_db_name"
        self.db_user = "your_db_user"
        self.db_password = "your_db_pwd"
        self.db_port = "db_port"

    def analyze_connections_by_loyalty(self, account_in_analysis, platform, connection_type):
        dao = DatabaseDAO(self.db_host, self.db_name, self.db_user, self.db_password, self.db_port)
        rows = dao.get_accounts_connected(account_in_analysis, platform, connection_type)
        all_contents = dao.count_contents_created_by_account(account_in_analysis, platform)
        
        loyalty = []
        for row in rows:
            reactions = dao.count_contents_with_reactions_from_account(row[0], account_in_analysis, platform)
            perc_of_contents_reacted_to = round((reactions*100)/all_contents, 2)
            mentions = dao.count_mentions_from_account(row[0], account_in_analysis, platform)
            references = dao.count_references_from_account(row[0], account_in_analysis, platform)

            loyalty.append(
                {
                    "account": row[0], 
                    "reactions": reactions, 
                    f'% of contents reacted to': f'{perc_of_contents_reacted_to}%',
                    "mentions": mentions, 
                    "references": references,
                    "loyalty": round(statistics.mean([reactions, mentions, references]), 2)
                }
            )
        
        return sorted(loyalty, key=lambda x: x['loyalty'], reverse=True)

if __name__ == "__main__":
    cl = LoyalConsumers()
    loyalt = cl.analyze_connections_by_loyalty(account_in_analysis='1', platform='Instagram', connection_type='Follow')
    for el in loyalt:
        print(el)

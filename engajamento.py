from datetime import datetime
from databaseDAO import DatabaseDAO
import matplotlib.pyplot as plt

class Engagement:
    def __init__(self):
        self.db_host = "your_db_host"
        self.db_name = "your_db_name"
        self.db_user = "your_db_user"
        self.db_password = "your_db_pwd"
        self.db_port = "db_port"
        self.dao = DatabaseDAO(self.db_host, self.db_name, self.db_user, self.db_password, self.db_port)

    def fetch_data(self):
        try:
            rows = self.dao.get_all_social_media_contents_for_engagement_analysis()
            return rows
        
        except Exception as e:
            print(f"Error: {e}")
            return []

    def f_weight(self, interaction_sum, eta, n):
        return 1 / ((interaction_sum / eta) * n)

    def calculate_engagement(self, rows):
        share_sum = sum(row[1] for row in rows)
        quote_sum = sum(row[2] for row in rows)
        like_sum = sum(row[3] for row in rows)
        reply_sum = sum(row[4] for row in rows)
        react_sum = sum(row[5] for row in rows)
        
        eta = share_sum + quote_sum + like_sum + reply_sum + react_sum
        n = 5   # types of interactions considered (share, quote, like, reply and react)
        
        share_weight = self.f_weight(share_sum, eta, n)
        quote_weight = self.f_weight(quote_sum, eta, n)
        like_weight = self.f_weight(like_sum, eta, n)
        reply_weight = self.f_weight(reply_sum, eta, n)
        react_weight = self.f_weight(react_sum, eta, n)
        
        engagement = [
            {
                "content": row[0], 
                "share": row[1], "quote": row[2], "like": row[3], "reply": row[4], "react": row[5],
                "engagement": round(
                    row[1]*share_weight + row[2]*quote_weight + row[3]*like_weight + row[4]*reply_weight + row[5]*react_weight, 
                    2
                )
            }
            for row in rows
        ]

        return sorted(engagement, key=lambda x: x['engagement'], reverse=True)
    
    def plot_engagement_in_time_by_account(self, account_id):
        try:
            rows = self.dao.get_social_media_contents_created_by_account(account_id)
            e = self.calculate_engagement(rows)

            dates = []
            engagements = []
            for item in e:
                timestamp = self.dao.get_date_of_creation_for_content(item['content'])
                date = timestamp.strftime('%Y-%m-%d')
                dates.append(date)
                engagements.append(item['engagement'])

            dates_sorted, engagements_sorted = zip(*sorted(zip(dates, engagements)))
            dates_sorted = [(datetime.strptime(date, '%Y-%m-%d')).strftime('%d-%m-%Y') for date in dates_sorted]

            plt.figure(figsize=(8, 6))

            bars = plt.bar(dates_sorted, engagements_sorted, align='center', alpha=0.5)
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{height}', ha='center', va='bottom')

            plt.xticks(rotation=45)
            plt.xlabel('Date')
            plt.ylabel('Engagement')
            plt.title('Engagement of social media contents by time')
            plt.tight_layout()
            plt.show()
        
        except Exception as e:
            print(f"Error: {e}")
            return

if __name__ == "__main__":
    e = Engagement()
    rows = e.fetch_data()
    if rows:
        engajamento = e.calculate_engagement(rows)
        for el in engajamento:
            print(el)
    else:
        print("No data found.")

    e.plot_engagement_in_time_by_account('1')

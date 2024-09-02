import math
import statistics
from databaseDAO import DatabaseDAO
from influenciadores import Influencers
from matching_expressions import MatchingExpressions
from sentiment import SentimentAnalysis
from graphs import Graph
import pandas as pd

class Viralizar:
    def __init__(self):
        self.db_host = "your_db_host"
        self.db_name = "your_db_name"
        self.db_user = "your_db_user"
        self.db_password = "your_db_pwd"
        self.db_port = "db_port"

    def fetch_data_for_viral_potential(self):
        try:
            dao = DatabaseDAO(self.db_host, self.db_name, self.db_user, self.db_password, self.db_port)
            rows = dao.get_all_social_media_contents_for_viral_potential()
            return rows
        
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return []
        
    def fetch_data_for_virality_metrics(self, initial_date, final_date):
        try:
            dao = DatabaseDAO(self.db_host, self.db_name, self.db_user, self.db_password, self.db_port)
            rows = dao.get_all_social_media_contents_for_virality_metrics(initial_date, final_date)
            return rows
        
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return []
        
    def get_all_contents_by_creator(self, account_id):
        try:
            dao = DatabaseDAO(self.db_host, self.db_name, self.db_user, self.db_password, self.db_port)
            rows = dao.get_social_media_contents_created_by_account(account_id)
            return rows
        
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return []
        
    def count_followers_of_creator(self, account_id):
        try:
            dao = DatabaseDAO(self.db_host, self.db_name, self.db_user, self.db_password, self.db_port)
            row = dao.count_followers_of_account(account_id)
            return row
        
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return 0
    
    # Calculating viral potential

    def set_properties_scores(
        self, 
        author_credibility, 
        refutation_statements, 
        rumor_allegations, 
        justification, 
        call_to_action, 
        presence_of_image, 
        presence_of_URL, 
        evokes_emotion
    ):
        pscores = {
            "author credibility": float(author_credibility),
            "refuting something or someone": float(refutation_statements),
            "rumor allegations": float(rumor_allegations),
            "justification": float(justification),
            "call to action": float(call_to_action),
            "presence of image": float(presence_of_image),
            "presence of URL": float(presence_of_URL),
            "evokes emotion": float(evokes_emotion),
        }

        return pscores

    def calculate_viral_potential_based_on_properties(self, contents, pscores):
        potential = []
        for content in contents:
            smc_id, smc_url, smc_text, smc_media_count, smc_mention_count, a_verified, a_followers = content
            
            score = 0

            if a_verified == True: 
                score += 0.25 * pscores["author credibility"]
            if a_followers > 10000: 
                score += 0.25 * pscores["author credibility"]
            elif a_followers > 500000: 
                score += 0.50 * pscores["author credibility"]
            elif a_followers > 1000000: 
                score += 0.75 * pscores["author credibility"]

            matcher = MatchingExpressions()

            probability_of_having_property_1 = matcher.matches_expressions_from_refutation_statements(smc_text)
            score += probability_of_having_property_1 * 0.9 * pscores["refuting something or someone"]
            if smc_mention_count > 0: score += 0.1 * pscores["refuting something or someone"]

            probability_of_having_property_2 = matcher.matches_expressions_from_rumor_allegations(smc_text)
            score += probability_of_having_property_2 * pscores["rumor allegations"]

            probability_of_having_property_3 = matcher.matches_expressions_from_justification(smc_text)
            score += probability_of_having_property_3 * pscores["justification"]

            probability_of_having_property_4 = matcher.matches_expressions_from_call_to_action(smc_text)
            score += probability_of_having_property_4 * pscores["call to action"]

            score += pscores["presence of image"] if smc_media_count > 0 else 0
            
            score += pscores["presence of URL"] if smc_url != None and smc_url != "" else 0

            sa = SentimentAnalysis()

            sentiment = sa.calculate_polarity(smc_text)
            if sentiment == 'neg': 
                score += pscores["evokes emotion"]
            elif sentiment == 'pos': 
                score += 0.5 * pscores["evokes emotion"]

            potential.append({
                "content": smc_id, 
                "author credibility": ("verified" if a_verified else "not verified") + f" ({a_followers} followers)",
                "text": smc_text,
                "refuting something or someone": probability_of_having_property_1,
                "rumor allegations": probability_of_having_property_2,
                "justification": probability_of_having_property_3,
                "call to action": probability_of_having_property_4,
                "presence of image": "yes" if smc_media_count > 0 else "no",
                "presence of URL": "yes" if smc_url != None and smc_url != "" else "no",
                "evokes emotion": sentiment,
                "viral potential": round(score/sum(pscores.values()), 2)
            })
        
        return sorted(potential, key=lambda x: x['viral potential'], reverse=True)

    # Identifying viral contents

    def calculate_virality_metrics(self, contents):
        metrics = []
        for c in contents:
            smc_id, creator_id, share_count, quote_count, like_count, reply_count, react_count = c
            I = sum([share_count, quote_count, like_count, reply_count, react_count])
            all_contents_by_creator = self.get_all_contents_by_creator(creator_id)
            contents_with_inferior_I = 0
            I_of_all_c = []
            for other_c in all_contents_by_creator:
                _smc_id, _share_count, _quote_count, _like_count, _reply_count, _react_count = other_c
                _I = sum([_share_count, _quote_count, _like_count, _reply_count, _react_count])
                I_of_all_c.append(_I)
                if I > _I: 
                    contents_with_inferior_I += 1
            
            n_of_contents = len(all_contents_by_creator)
            I_mean = statistics.mean(I_of_all_c)
            I_median = statistics.median(I_of_all_c)
            followers = self.count_followers_of_creator(creator_id)
            
            metrics.append(
                {
                    "content": smc_id,
                    "% of contents with inferior I": f'{round((contents_with_inferior_I*100)/n_of_contents, 2)}%',
                    "I": I,
                    "I / Median": round(I/I_median, 2) if I_median > 0 else "No interactions",
                    "I / Mean": round(I/I_mean, 2) if I_mean > 0 else "No interactions",
                    "I / Connections": round(I/followers, 2) if followers > 0 else "No connections",
                    "log(I / Connections)": round(math.log(I/followers), 2) if followers > 0 else "No connections",
                }
            )

        return sorted(metrics, key=lambda x: x['I'], reverse=True)

    def generate_graph_of_content_reach(self, content_id, platform, connection_type):
        try:
            dao = DatabaseDAO(self.db_host, self.db_name, self.db_user, self.db_password, self.db_port)
            accounts = dao.get_all_accounts_that_interacted_with_content(content_id)
            print(accounts)
            connections = dao.get_connections(platform, connection_type)
            print(connections)
            G = Graph().gen_DiGraph(accounts, connections)
            return G
            
        except Exception as e:
            print(f"Error: {e}")
            return None
        
    def calculate_levels_reached_by_content(self, G, s):
        return Graph().bfs(G, s)

    def save_to_excel(self, data, file_name):
        df = pd.DataFrame(data)
        df.to_excel(file_name, index=False)


if __name__ == "__main__":
    v = Viralizar()
  
    #contents_for_viral_potential = v.fetch_data_for_viral_potential()
    #scores = v.set_properties_scores(1, 1, 1, 1, 1, 1, 1, 1)
    #potential = v.calculate_viral_potential_based_on_properties(contents_for_viral_potential, scores)
    #for el in potential:
    #    print(el)
    
    #v.save_to_excel(potential, "potential.xlsx")

    #contents_for_virality_metrics = v.fetch_data_for_virality_metrics('2024-01-01', '2024-06-01')
    #metrics = v.calculate_virality_metrics(contents_for_virality_metrics)
    #for el in metrics:
    #    print(el)
    
    #v.save_to_excel(metrics, "metrics.xlsx")

    i = Influencers()
    Gi = i.generate_graph_from_connections("Instagram", "Follow")
    Graph().view_graph(Gi)
    Gv = v.generate_graph_of_content_reach('1', 'Instagram', 'Follow')
    Graph().view_graph(Gv)
    reversed_Gv = Gv.reverse(copy=True)
    levels = v.calculate_levels_reached_by_content(reversed_Gv, ('1'))
    print(f'levels reached: {levels}')

import statistics
import networkx as nx
from databaseDAO import DatabaseDAO
from engajamento import Engagement
from graphs import Graph

class Influencers:
    def __init__(self):
        self.db_host = "your_db_host"
        self.db_name = "your_db_name"
        self.db_user = "your_db_user"
        self.db_password = "your_db_pwd"
        self.db_port = "db_port"
        
    def generate_graph_from_connections(self, platform, connection_type):
        try:
            dao = DatabaseDAO(self.db_host, self.db_name, self.db_user, self.db_password, self.db_port)
            connections = dao.get_connections(platform, connection_type)
            G = Graph().gen_DiGraph(connections, None)
            return G
            
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def betweenness_and_degree(self, G):
        betweenness_centrality = nx.betweenness_centrality(G)
        betweenness_and_degree = []
        for node, bc in betweenness_centrality.items():
            betweenness_and_degree.append({
                "node": node, "in_degree": G.in_degree(node), "out_degree": G.out_degree(node), 
                "betweenness centrality": bc
            })
        
        return betweenness_and_degree
    
    def average_engagement_by_account(self, accounts):
        dao = DatabaseDAO(self.db_host, self.db_name, self.db_user, self.db_password, self.db_port)
        all_social_media_contents = []
        social_media_contents_by_account = []

        for account in accounts:
            social_media_contents = dao.get_social_media_contents_created_by_account(account)
            if social_media_contents:
                all_social_media_contents.extend(social_media_contents)
                contents_id = [smc[0] for smc in social_media_contents]
                social_media_contents_by_account.append({"account": account, "social_media_contents": contents_id})
            else:
                social_media_contents_by_account.append({"account": account, "social_media_contents": None})

        e = Engagement()
        eng = e.calculate_engagement(all_social_media_contents)

        eng_map = {item['content']: item['engagement'] for item in eng}
        average_engagement_by_account = []

        for account in social_media_contents_by_account:
            smcs = account['social_media_contents']
            if smcs:
                total_engagement = sum(eng_map[smc] for smc in smcs if smc in eng_map)
                average_engagement = total_engagement / len(smcs)
            else:
                average_engagement = 0

            average_engagement_by_account.append({'account': account['account'], 'average engagement': round(average_engagement, 2)})

        return average_engagement_by_account

    def analyze_accounts_as_influencers(self, G):
        betweenness_and_degree = self.betweenness_and_degree(G)

        accounts = [el["node"] for el in betweenness_and_degree]
        average_engagement_by_account = self.average_engagement_by_account(accounts)

        max_bc = max(betweenness_and_degree, key=lambda x: x["betweenness centrality"])["betweenness centrality"]
        min_bc = min(betweenness_and_degree, key=lambda x: x["betweenness centrality"])["betweenness centrality"]
        max_in_dg = max(betweenness_and_degree, key=lambda x: x["in_degree"])["in_degree"]
        min_in_dg = min(betweenness_and_degree, key=lambda x: x["in_degree"])["in_degree"]
        max_avg_eng = max(average_engagement_by_account, key=lambda x: x["average engagement"])["average engagement"]
        min_avg_eng = min(average_engagement_by_account, key=lambda x: x["average engagement"])["average engagement"]

        influencer_analysis = []
        for bd_item in betweenness_and_degree:
            account_id = bd_item["node"]
            for ae_item in average_engagement_by_account:
                if ae_item["account"] == account_id:
                    betweenness = bd_item["betweenness centrality"]
                    normalized_bc = (betweenness - min_bc) / (max_bc - min_bc) if max_bc != min_bc else 0.5
                    in_degree = bd_item["in_degree"]
                    normalized_in_degree = (in_degree - min_in_dg) / (max_in_dg - min_in_dg) if max_in_dg != min_in_dg else 0.5
                    out_degree = bd_item["out_degree"]
                    avg_eng = ae_item["average engagement"]
                    normalized_avg_eng = (avg_eng - min_avg_eng) / (max_avg_eng - min_avg_eng) if max_avg_eng != min_avg_eng else 0.5
                    
                    influencer_analysis.append({
                        "account": account_id,
                        "betweenness": round(betweenness, 3),
                        "in_degree": in_degree,
                        "out_degree": out_degree,
                        "average engagement of contents": avg_eng,
                        "normalized betweenness": round(normalized_bc, 2),
                        "normalized in_degree": round(normalized_in_degree, 2),
                        "normalized average engagement": round(normalized_avg_eng, 2),
                        "influence": round(statistics.mean([normalized_bc, normalized_in_degree, normalized_avg_eng]), 2)
                    })
                    break

        return sorted(influencer_analysis, key=lambda x: x['influence'], reverse=True)

if __name__ == "__main__":
    i = Influencers()
    G = i.generate_graph_from_connections("Instagram", "Follow")
    #Graph().view_graph(G)
    influencer_analysis = i.analyze_accounts_as_influencers(G)
    for el in influencer_analysis:
        print(el)

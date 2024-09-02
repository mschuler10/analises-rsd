import psycopg2

class DatabaseDAO:
    def __init__(self, db_host, db_name, db_user, db_password, db_port):
        self.db_host = db_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_port = db_port

    # Viralizar
    def get_all_social_media_contents_for_viral_potential(self):
        try:
            conn = psycopg2.connect(
                host=self.db_host,
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                port=self.db_port
            )
            cur = conn.cursor()

            sql = """
            SELECT 
                smc.id AS content_id, smc.URL AS content_url, smc.text AS content_text,
                COUNT(DISTINCT m.id) AS media_count,
                COUNT(DISTINCT mnt.fk_account_id) AS mention_count,
                a.verified AS account_verified, a.followers AS account_followers
            FROM 
                Creates cr
            JOIN 
                Social_Media_Content smc ON cr.fk_Social_Media_Content_id = smc.id
            LEFT JOIN 
                Media m ON m.fk_Social_Media_Content_PK = smc.id
            LEFT JOIN 
                Mentions mnt ON mnt.fk_Social_Media_Content_id = smc.id
            LEFT JOIN 
                Account a ON cr.fk_Account_id = a.id
            GROUP BY 
                smc.id, smc.URL, smc.text, a.verified, a.followers;
            """

            cur.execute(sql)
            rows = cur.fetchall()

            cur.close()
            conn.close()

            return rows

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return None

    def get_all_social_media_contents_for_virality_metrics(self, initial_date, final_date):
        try:
            conn = psycopg2.connect(
                host=self.db_host,
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                port=self.db_port
            )
            cur = conn.cursor()

            sql = """
            SELECT 
                smc.id, cr.fk_Account_id, smc.share_count, smc.quote_count, smc.like_count, 
                smc.reply_count, COUNT(r.fk_account_id) AS react_count
            FROM 
                Social_Media_Content smc
            LEFT JOIN
                Creates cr ON cr.fk_Social_Media_Content_id = smc.id
            LEFT JOIN 
                Reacts r ON r.fk_Social_Media_Content_id = smc.id
            WHERE 
                cr.timestamp BETWEEN %s AND %s
            GROUP BY 
                smc.id, cr.fk_Account_id, smc.share_count, smc.quote_count, smc.like_count, 
                smc.reply_count;
            """

            cur.execute(sql, (initial_date, final_date))
            rows = cur.fetchall()

            cur.close()
            conn.close()

            return rows

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return None

    def get_creator_of_content(self, content_id):
        try:
            conn = psycopg2.connect(
                host=self.db_host,
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                port=self.db_port
            )
            cur = conn.cursor()

            sql = """
            SELECT 
                cr.fk_account_platform, cr.fk_account_id
            FROM 
                Creates cr
            WHERE 
                cr.fk_Social_Media_Content_id = %s;
            """   

            cur.execute(sql, (content_id,))
            row = cur.fetchone()

            cur.close()
            conn.close()

            return row[0] if row else None

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return None
        
    def get_all_accounts_that_interacted_with_content(self, content_id):
        try:
            conn = psycopg2.connect(
                host=self.db_host,
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                port=self.db_port
            )
            cur = conn.cursor()        

            sql = """
            (SELECT 
                r.fk_account_platform, r.fk_account_id
            FROM 
                Reacts r
            WHERE 
                r.fk_Social_Media_Content_id = %s)
            UNION
            (SELECT 
                cr.fk_account_platform, cr.fk_account_id
            FROM 
                References_Table rt
            LEFT JOIN 
                Creates cr ON cr.fk_Social_Media_Content_id = rt.fk_Social_Media_Content_1
            WHERE 
                rt.fk_Social_Media_Content_2 = %s)
            UNION
            (SELECT 
                cr.fk_account_platform, cr.fk_account_id
            FROM 
                Creates cr
            WHERE 
                cr.fk_Social_Media_Content_id = %s);
            """

            cur.execute(sql, (content_id, content_id, content_id))
            rows = cur.fetchall()

            cur.close()
            conn.close()

            return rows

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return None
        
    # Engajamento
    def get_all_social_media_contents_for_engagement_analysis(self):
        try:
            conn = psycopg2.connect(
                host=self.db_host,
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                port=self.db_port
            )
            cur = conn.cursor()

            sql = """
            SELECT 
                smc.id, smc.share_count, smc.quote_count, smc.like_count, smc.reply_count,
                COUNT(r.fk_account_id) AS react_count
            FROM 
                Social_Media_Content smc
            LEFT JOIN 
                Reacts r ON r.fk_Social_Media_Content_id = smc.id
            GROUP BY 
                smc.id, smc.share_count, smc.quote_count, smc.like_count, smc.reply_count;
            """
            
            cur.execute(sql)
            rows = cur.fetchall()

            cur.close()
            conn.close()

            return rows

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return None

    def get_date_of_creation_for_content(self, content_id):
        try:
            conn = psycopg2.connect(
                host=self.db_host,
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                port=self.db_port
            )
            cur = conn.cursor()

            sql = """
            SELECT 
                cr.timestamp
            FROM 
                Creates cr
            WHERE 
                cr.fk_Social_Media_Content_id = %s;
            """   

            cur.execute(sql, (content_id,))
            row = cur.fetchone()

            cur.close()
            conn.close()

            return row[0] if row else None

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return None
        
    # Influencers
    def get_connections(self, platform, connection_type):
        try:
            conn = psycopg2.connect(
                host=self.db_host,
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                port=self.db_port
            )
            cur = conn.cursor()

            sql = """
            SELECT 
                fk_Account_platform_1, fk_Account_id_1, fk_Account_platform_2, fk_Account_id_2
            FROM 
                Connects
            WHERE
                fk_Account_platform_1 = %s AND fk_Account_platform_1 = fk_Account_platform_2 AND type = %s;
            """
            
            cur.execute(sql, (platform, connection_type))
            rows = cur.fetchall()

            cur.close()
            conn.close()

            return rows

        except Exception as e:
            print(f"Ocorreu um erro 266: {e}")
            return None
        
    def get_social_media_contents_created_by_account(self, account_id):
        try:
            conn = psycopg2.connect(
                host=self.db_host,
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                port=self.db_port
            )
            cur = conn.cursor()

            sql = """
            SELECT 
                smc.id, smc.share_count, smc.quote_count, smc.like_count, smc.reply_count,
                COUNT(r.fk_account_id) AS react_count
            FROM 
                Social_Media_Content smc
            LEFT JOIN 
                Reacts r ON r.fk_Social_Media_Content_id = smc.id
            WHERE 
                smc.id IN (
                    SELECT smc.id
                    FROM Social_Media_Content smc
                    JOIN Creates cr ON cr.fk_Social_Media_Content_id = smc.id
                    WHERE cr.fk_Account_id = %s
                )
            GROUP BY 
                smc.id, smc.share_count, smc.quote_count, smc.like_count, smc.reply_count;
            """
            
            cur.execute(sql, (account_id,))
            rows = cur.fetchall()

            cur.close()
            conn.close()

            return rows

        except Exception as e:
            print(f"Ocorreu um erro 308: {e}")
            return None

    def count_followers_of_account(self, account_id):
        try:
            conn = psycopg2.connect(
                host=self.db_host,
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                port=self.db_port
            )
            cur = conn.cursor()

            sql = """
            SELECT followers 
            FROM Account 
            WHERE id = %s
            """
            
            cur.execute(sql, (account_id,))
            row = cur.fetchone()

            cur.close()
            conn.close()

            if row:
                return row[0]
            else:
                return None

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return None
        
    # Consumidores Leais
    def get_accounts_connected(self, account_id, platform, connection_type):
        try:
            conn = psycopg2.connect(
                host=self.db_host,
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                port=self.db_port
            )
            cur = conn.cursor()

            sql = """
            SELECT 
                DISTINCT fk_Account_id_1
            FROM 
                Connects
            WHERE
                fk_Account_id_2 = %s AND
                fk_Account_platform_1 = %s AND 
                fk_Account_platform_1 = fk_Account_platform_2 AND 
                type = %s;
            """
            
            cur.execute(sql, (account_id, platform, connection_type))
            rows = cur.fetchall()

            cur.close()
            conn.close()

            return rows

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return None

    def count_contents_created_by_account(self, account_id, platform):
        try:
            conn = psycopg2.connect(
                host=self.db_host,
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                port=self.db_port
            )
            cur = conn.cursor()

            sql = """
            SELECT 
                COUNT(DISTINCT fk_Social_Media_Content_id)
            FROM 
                Creates cr
            WHERE 
                cr.fk_Account_id = %s AND fk_Account_platform = %s;
            """
            
            cur.execute(sql, (account_id, platform))
            row = cur.fetchone()

            cur.close()
            conn.close()

            return row[0] if row else 0

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return None
  
    def count_contents_with_reactions_from_account(self, account_id, content_creator_id, platform):
        try:
            conn = psycopg2.connect(
                host=self.db_host,
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                port=self.db_port
            )
            cur = conn.cursor()

            sql = """
            SELECT
                COUNT(DISTINCT r.fk_Social_Media_Content_id)
            FROM
                Reacts r
            WHERE 
                r.fk_Social_Media_Content_id IN (
                    SELECT cr.fk_Social_Media_Content_id
                    FROM Creates cr
                    WHERE cr.fk_Account_id = %s AND cr.fk_Account_platform = %s
                ) 
                AND
                r.fk_Account_id = %s AND r.fk_Account_platform = %s;
            """
            
            cur.execute(sql, (content_creator_id, platform, account_id, platform))
            row = cur.fetchone()

            cur.close()
            conn.close()

            return row[0] if row else 0

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return None
        
    def count_mentions_from_account(self, account_id, mentioned_account_id, platform):
        try:
            conn = psycopg2.connect(
                host=self.db_host,
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                port=self.db_port
            )
            cur = conn.cursor()

            sql = """
            SELECT
                COUNT(DISTINCT mnt.fk_Social_Media_Content_id)
            FROM
                Mentions mnt
            WHERE 
                mnt.fk_Social_Media_Content_id IN (
                    SELECT cr.fk_Social_Media_Content_id
                    FROM Creates cr
                    WHERE cr.fk_Account_id = %s AND cr.fk_Account_platform = %s
                ) 
                AND
                mnt.fk_Account_id = %s AND mnt.fk_Account_platform = %s;
            """
            
            cur.execute(sql, (account_id, platform, mentioned_account_id, platform))
            row = cur.fetchone()

            cur.close()
            conn.close()

            return row[0] if row else 0

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return None

    def count_references_from_account(self, account_id, referenced_account_id, platform):
        try:
            conn = psycopg2.connect(
                host=self.db_host,
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                port=self.db_port
            )
            cur = conn.cursor()

            sql = """
            SELECT
                COUNT(DISTINCT rt.fk_Social_Media_Content_1)
            FROM
                References_Table rt
            WHERE 
                rt.fk_Social_Media_Content_1 IN (
                    SELECT cr.fk_Social_Media_Content_id
                    FROM Creates cr
                    WHERE cr.fk_Account_id = %s AND cr.fk_Account_platform = %s
                ) 
                AND
                rt.fk_Social_Media_Content_2 IN (
                    SELECT cr.fk_Social_Media_Content_id
                    FROM Creates cr
                    WHERE cr.fk_Account_id = %s AND cr.fk_Account_platform = %s
                );
            """
            
            cur.execute(sql, (account_id, platform, referenced_account_id, platform))
            row = cur.fetchone()

            cur.close()
            conn.close()

            return row[0] if row else 0

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return None

import re

class MatchingExpressions:
    expressions = {
        "refutation_statements": {
            "nunca", "jamais", "falso", "não é verdade", "mentira", 
            "enganoso", "não acredito", "não concordo", "absurdo", 
            "inverdade", "não procede", "não é bem assim", "não é certo",
            "não está certo", "incorreto"
        },
        "rumor_allegations": {
            "boato", "rumor", "fofoca", "fake news", "ouvi dizer", 
            "estão dizendo", "acho que", "não se sabe", "dizem que", 
            "parece que", "supostamente", "é possível", "acredito que",
            "duvid", "acusa", "verdade", " veio à tona"
        },
        "justification": {
            "justifica", "motivo", "razão", "explicaç", "porque", 
            "por isso", "devido a", "em razão de", "porquê", "razões", 
            "razão", "motivos", "argument", "por causa"
        },
        "call_to_action": {
            "chame", "ligue", "peça", "faça", "visite", "participe", 
            "compre", "clique", "junte-se", "inscreva-se", "envie", 
            "aproveite", "descubra", "saiba mais", "veja", "denuncie", 
            "critique", "fale", "venha", "deixe", "perca", "olha"
        }
    }

    def __init__(self):
        pass

    def matches_expression(self, text, exp):
        regex_pattern = re.escape(exp)
        return bool(re.search(regex_pattern, text, re.IGNORECASE))

    def matches_expressions(self, text, category):
        count = sum(self.matches_expression(text, exp) for exp in self.expressions[category])
        return 0 if count == 0 else 0.5 if count == 1 else 1

    def matches_expressions_from_refutation_statements(self, text):
        return self.matches_expressions(text, "refutation_statements")

    def matches_expressions_from_rumor_allegations(self, text):
        return self.matches_expressions(text, "rumor_allegations")

    def matches_expressions_from_justification(self, text):
        return self.matches_expressions(text, "justification")

    def matches_expressions_from_call_to_action(self, text):
        return self.matches_expressions(text, "call_to_action")

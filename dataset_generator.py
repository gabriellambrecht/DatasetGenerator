import re
import csv

class DatasetGenerator:

    def __init__(self): 
        self.quantificador_masculino = DatasetGenerator.__get_quantificador_masculino()
        self.quantificador_masculino_plural = DatasetGenerator.__get_quantificador_masculino_plural()
        self.quantificador_feminino = DatasetGenerator.__get_quantificador_feminino()
        self.necessidade = DatasetGenerator.__get_necessidade()
        self.avaliacao_masculina = DatasetGenerator.__get_avaliacao_masculina()
        self.avaliacao_feminina = DatasetGenerator.__get_avaliacao_feminina()
        self.avaliacao_masculina_plural = DatasetGenerator.__get_avaliacao_masculina_plural()
        self.negacao = DatasetGenerator.__get_negacao()
        self.competencia_feminina = DatasetGenerator.__get_competencia_feminina()
        self.competencia_masculina = DatasetGenerator.__get_competencia_masculina()
        self.linhas_arquivo = DatasetGenerator.__busca_linhas_iniciais()
        self.linhas_geradas = []
        
    def generate_dataset(self):
        self.__executa_subtituicao()
        for linha in self.linhas_geradas:
            print('"' + linha[0] + '",' + str(linha[1]))

    def generate_dataset_as_file(self):
        self.__executa_subtituicao()
        f = open('dataset_feedback.csv', 'w', encoding='UTF8', newline='')
        writer = csv.writer(f)
        writer.writerows(self.linhas_geradas)
        f.close()

    def generate_dataset_as_text(self):
        self.__executa_subtituicao()
        for linha in self.linhas_geradas:
            frase = linha[0]
            polaridade = ""
            if linha[1] == -2 : polaridade = "Muito negativa"
            if linha[1] == -1 : polaridade = "Negativa"
            if linha[1] ==  0 : polaridade = "Neutra"
            if linha[1] ==  1 : polaridade = "Positiva"
            if linha[1] ==  2 : polaridade = "Muito positiva"
            print(frase + ", " + polaridade)

    def __executa_subtituicao(self):
        for linha in self.linhas_arquivo:
            self.__substituicao_recursiva(linha, 0)

    def __substituicao_recursiva(self, linha_original, nivel):
        if "[quantificador_masculino]" in linha_original: 
            for item in self.quantificador_masculino:
                linha_nova = linha_original.replace("[quantificador_masculino]", item)
                novo_nivel = nivel + self.quantificador_masculino[item]
                self.__substituicao_recursiva(linha_nova, novo_nivel)
        elif "[quantificador_masculino_plural]" in linha_original: 
            for item in self.quantificador_masculino_plural:
                linha_nova = linha_original.replace("[quantificador_masculino_plural]", item)
                novo_nivel = nivel + self.quantificador_masculino_plural[item]
                self.__substituicao_recursiva(linha_nova, novo_nivel)
        elif "[quantificador_feminino]" in linha_original: 
            for item in self.quantificador_feminino:
                linha_nova = linha_original.replace("[quantificador_feminino]", item)
                novo_nivel = nivel + self.quantificador_feminino[item]
                self.__substituicao_recursiva(linha_nova, novo_nivel)
        elif "[necessidade]" in linha_original: 
            for item in self.necessidade:
                linha_nova = linha_original.replace("[necessidade]", item)
                novo_nivel = nivel + self.necessidade[item]
                self.__substituicao_recursiva(linha_nova, novo_nivel)
        elif "[avaliacao_masculina]" in linha_original: 
            for item in self.avaliacao_masculina:
                linha_nova = linha_original.replace("[avaliacao_masculina]", item)
                novo_nivel = nivel + self.avaliacao_masculina[item]
                self.__substituicao_recursiva(linha_nova, novo_nivel)
        elif "[avaliacao_feminina]" in linha_original: 
            for item in self.avaliacao_feminina:
                linha_nova = linha_original.replace("[avaliacao_feminina]", item)
                novo_nivel = nivel + self.avaliacao_feminina[item]
                self.__substituicao_recursiva(linha_nova, novo_nivel)
        elif "[avaliacao_masculina_plural]" in linha_original: 
            for item in self.avaliacao_masculina_plural:
                linha_nova = linha_original.replace("[avaliacao_masculina_plural]", item)
                novo_nivel = nivel + self.avaliacao_masculina_plural[item]
                self.__substituicao_recursiva(linha_nova, novo_nivel)
        elif "[negacao]" in linha_original: 
            for item in self.negacao:
                linha_nova = linha_original.replace("[negacao]", item)
                if nivel == 0: nivel = 1
                if item == "Não":
                    novo_nivel = nivel * -1
                else:
                    novo_nivel = nivel
                self.__substituicao_recursiva(linha_nova, novo_nivel)
        elif "[competencia_feminina]" in linha_original: 
            for item in self.competencia_feminina:
                linha_nova = linha_original.replace("[competencia_feminina]", item)
                self.__substituicao_recursiva(linha_nova, nivel)
        elif "[competencia_masculina]" in linha_original: 
            for item in self.competencia_masculina:
                linha_nova = linha_original.replace("[competencia_masculina]", item)
                self.__substituicao_recursiva(linha_nova, nivel)
        else :
            linha_original = linha_original.strip().capitalize()
            linha_original = re.sub("\s\s+", " ", linha_original)
            self.linhas_geradas.append([linha_original, nivel])


    @staticmethod
    def __busca_linhas_iniciais():
        with open("lista_inicial_frases.txt") as file:
            linhas_arquivo = file.readlines()
            linhas_arquivo = [linha.rstrip() for linha in linhas_arquivo]
        return linhas_arquivo 

    @staticmethod
    def __get_quantificador_masculino():
        return {"pouquíssimo": -2,
                "pouco"      : -2,
                ""           :  1,
                "muito"      :  2,
                "muitíssimo" :  2}

    @staticmethod
    def __get_quantificador_masculino_plural():
        return {"pouquíssimos": -2,
                "poucos"      : -2,
                ""            :  1,
                "muitos"      :  2,
                "muitíssimos" :  2}

    @staticmethod
    def __get_quantificador_feminino():
        return {"pouquíssima": -2,
                "pouca"      : -2,
                ""           :  1,
                "muita"      :  2,
                "muitíssima" :  2}

    @staticmethod
    def __get_necessidade():
        return {"dispensável"  : -1,
                "necessário"   :  1,
                "importante"   :  1,
                "essencial"    :  2,
                "indispensável":  2}

    @staticmethod
    def __get_avaliacao_masculina():
        return {"péssimo"           : -2,
                "ruim"              : -1,
                "abaixo do esperado": -1,
                "baixo"             : -1,
                "mediano"           :  0,
                "aceitável"         :  0,
                "na média"          :  0,
                "acima do esperado" :  1,
                "bom"               :  1,
                "alto"              :  1,
                "ótimo"             :  2}

    @staticmethod
    def __get_avaliacao_feminina():
        return {"péssima"           : -2,
                "ruim"              : -1,
                "abaixo do esperado": -1,
                "baixa"             : -1,
                "mediana"           :  0,
                "aceitável"         :  0,
                "na média"          :  0,
                "acima do esperado" :  1,
                "boa"               :  1,
                "alta"              :  1,
                "ótima"             :  2}

    @staticmethod
    def __get_avaliacao_masculina_plural():
        return {"péssimos"          : -2,
                "ruins"             : -1,
                "abaixo do esperado": -1,
                "medianos"          :  0,
                "aceitáveis"        :  0,
                "na média"          :  0,
                "acima do esperado" :  1,
                "bons"              :  1,
                "altos"             :  1,
                "ótimos"            :  2}

    @staticmethod
    def __get_negacao():
        return {"",
                "Não"}

    #Tem muita
    @staticmethod
    def __get_competencia_feminina():
        return {"criatividade",
                "performance",
                "dedicação",
                "organização",
                "assiduidade",
                "responsabilidade",
                "experiência",
                "clareza",
                "liderança"
                "visão estratégica",
                "visão gerencial",
                "capacidade técnica",
                "influência na empresa",
                "comunicação",
                "facilidade com os problemas encontrados",
                "inteligência social e emocional",
                "educação",
                "inovação",
                "desenvoltura",
                "confiabilidade",
                "ética",
                "perspicácia",
                "competências técnicas",
                "competências comportamentais",
                "qualidades"}

    #Tem muito
    @staticmethod
    def __get_competencia_masculina():
        return {"conhecimento técnico", 
                "comprometimento",
                "desempenho",
                "esforço",
                "trabalho colaborativo",
                "compromisso com o trabalho",
                "respeito",
                "perfil de gestor",
                "planejamento pessoal",
                "planejamento das atividades",
                "raciocínio lógico"}
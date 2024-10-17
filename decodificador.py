class DecodificadorRISCV:
    def __init__(self, caminho_do_arquivo="codigo.hex"):
        self.caminho_do_arquivo = caminho_do_arquivo
        self.instrucoes = []
        self.instrucoes_com_nops = []
        self.estatisticas = {
            'total': 0,
            'alu': 0,
            'jump': 0,
            'branch': 0,
            'memory': 0,
            'other': 0,
            'nops_inseridos': 0  # Estatística de NOPs
        }

    def __ler_instrucoes_do_arquivo(self):
        with open(self.caminho_do_arquivo, 'r') as arquivo:
            for linha in arquivo:
                instrucao_em_hexadecimal = linha.strip()
                self.instrucoes.append(instrucao_em_hexadecimal)

    def __decodificar_instrucoes(self, instrucao_em_hexadecimal):
        instrucao_em_binario = bin(int(instrucao_em_hexadecimal, 16))[2:].zfill(32)
        opcode = instrucao_em_binario[-7:]
        
        if opcode == '0110011':  # Tipo R (ALU)
            self.estatisticas['alu'] += 1
            return self.__decodificar_instrucao_do_tipo_r(instrucao_em_binario)
        elif opcode == '0010011':  # Tipo I (ALU Immediate)
            self.estatisticas['alu'] += 1
            return self.__decodificar_instrucao_do_tipo_i(instrucao_em_binario)
        elif opcode == '1101111':  # Tipo J (Jump - JAL)
            self.estatisticas['jump'] += 1
            return self.__decodificar_instrucao_do_tipo_j(instrucao_em_binario)
        elif opcode == '1100111':  # Tipo I (Jump - JALR)
            self.estatisticas['jump'] += 1
            return self.__decodificar_instrucao_do_tipo_i(instrucao_em_binario)
        elif opcode == '1100011':  # Tipo B (Branch)
            self.estatisticas['branch'] += 1
            return self.__decodificar_instrucao_do_tipo_b(instrucao_em_binario)
        elif opcode == '0000011':  # Tipo I (Load)
            self.estatisticas['memory'] += 1
            return self.__decodificar_instrucao_do_tipo_i(instrucao_em_binario)
        elif opcode == '0100011':  # Tipo S (Store)
            self.estatisticas['memory'] += 1
            return self.__decodificar_instrucao_do_tipo_s(instrucao_em_binario)
        elif opcode == '0010111' or opcode == '0110111':  # Tipo U (LUI, AUIPC)
            self.estatisticas['other'] += 1
            return self.__decodificar_instrucao_do_tipo_u(instrucao_em_binario)
        else:
            self.estatisticas['other'] += 1
            return f"Formato desconhecido para a instrução {instrucao_em_hexadecimal}"

    def __decodificar_instrucao_do_tipo_r(self, instrucao_em_binario):
        rd = int(instrucao_em_binario[20:25], 2)
        f3 = int(instrucao_em_binario[17:20], 2)
        rs1 = int(instrucao_em_binario[12:17], 2)
        rs2 = int(instrucao_em_binario[7:12], 2)
        f7 = int(instrucao_em_binario[0:7], 2)
        return f"Formato = R, rd = {rd}, f3 = {f3}, rs1 = {rs1}, rs2 = {rs2}, f7 = {f7}"

    def __decodificar_instrucao_do_tipo_i(self, instrucao_em_binario):
        rd = int(instrucao_em_binario[20:25], 2)
        f3 = int(instrucao_em_binario[17:20], 2)
        rs1 = int(instrucao_em_binario[12:17], 2)
        imm = int(instrucao_em_binario[0:12], 2)
        return f"Formato = I, rd = {rd}, f3 = {f3}, rs1 = {rs1}, imed = {imm}"

    def __decodificar_instrucao_do_tipo_s(self, instrucao_em_binario):
        imm = (int(instrucao_em_binario[0:7], 2) << 5) | int(instrucao_em_binario[20:25], 2)
        f3 = int(instrucao_em_binario[17:20], 2)
        rs1 = int(instrucao_em_binario[12:17], 2)
        rs2 = int(instrucao_em_binario[7:12], 2)
        return f"Formato = S, f3 = {f3}, rs1 = {rs1}, rs2 = {rs2}, imed = {imm}"

    def __decodificar_instrucao_do_tipo_b(self, instrucao_em_binario):
        imm = (int(instrucao_em_binario[0], 2) << 12) | (int(instrucao_em_binario[24:25], 2) << 11) | \
              (int(instrucao_em_binario[1:7], 2) << 5) | int(instrucao_em_binario[20:24], 2)
        f3 = int(instrucao_em_binario[17:20], 2)
        rs1 = int(instrucao_em_binario[12:17], 2)
        rs2 = int(instrucao_em_binario[7:12], 2)
        return f"Formato = B, f3 = {f3}, rs1 = {rs1}, rs2 = {rs2}, imed = {imm}"

    def __decodificar_instrucao_do_tipo_u(self, instrucao_em_binario):
        rd = int(instrucao_em_binario[20:25], 2)
        imm = int(instrucao_em_binario[0:20], 2)
        return f"Formato = U, rd = {rd}, imed = {imm}"

    def __decodificar_instrucao_do_tipo_j(self, instrucao_em_binario):
        rd = int(instrucao_em_binario[20:25], 2)
        imm = (int(instrucao_em_binario[0], 2) << 20) | (int(instrucao_em_binario[12:20], 2) << 12) | \
              (int(instrucao_em_binario[11], 2) << 11) | int(instrucao_em_binario[1:11], 2)
        return f"Formato = J, rd = {rd}, imed = {imm}"

    def __detectar_conflito(self, instrucao_atual, instrucao_anterior):
        # Convertendo as instruções para binário
        instrucao_atual_binario = bin(int(instrucao_atual, 16))[2:].zfill(32)
        instrucao_anterior_binario = bin(int(instrucao_anterior, 16))[2:].zfill(32)
        
        # Extrair os registros rs1 e rs2 da instrução atual e rd da instrução anterior
        rs1_atual = int(instrucao_atual_binario[12:17], 2)  # rs1 da instrução atual
        rs2_atual = int(instrucao_atual_binario[7:12], 2)   # rs2 da instrução atual (se for tipo R)
        rd_anterior = int(instrucao_anterior_binario[20:25], 2)  # rd da instrução anterior
        
        # Verificar se a instrução atual depende da anterior (conflito de dados)
        if rs1_atual == rd_anterior or rs2_atual == rd_anterior:
            return True
        return False


    def resolver_conflitos(self):
        # Processar instruções e inserir NOPs onde necessário
        for i in range(len(self.instrucoes)):
            if i > 0:
                if self.__detectar_conflito(self.instrucoes[i], self.instrucoes[i-1]):
                    self.instrucoes_com_nops.append('00000013')  # Inserir NOP (ADDI x0, x0, 0)
                    self.estatisticas['nops_inseridos'] += 1
            self.instrucoes_com_nops.append(self.instrucoes[i])

    def classificar_instrucoes(self):
        self.__ler_instrucoes_do_arquivo()
        for inst in self.instrucoes:
            self.__decodificar_instrucoes(inst)
        self.estatisticas['total'] = len(self.instrucoes)

    def printar_estatisticas(self):
        print(f"Estatísticas: {self.estatisticas}")

    def printar_instrucoes(self):
        for inst in self.instrucoes_com_nops:
            decoded = self.__decodificar_instrucoes(inst) if inst != 'NOP' else 'NOP'
            print(decoded)

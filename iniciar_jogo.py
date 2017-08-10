# coding: utf-8
# Lucas de Medeiros Nunes Fernandes, 117110210
# lucas.medeiros.fernandes@ccc.ufcg.edu.br
# Miniprojeto 1, Damas

import pygame
from pygame.locals import *

pygame.init()

# VARIÁVEIS DE VALOR CONSTANTE
LARGURA = 800
ALTURA = 600

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA = (100, 100, 100)
VERMELHO = (120, 0, 0)
VERDE_ESCURO = (0, 120, 0)
VERDE_CLARO = (0, 255, 0)
VERMELHO_CLARO = (255, 0, 0)
AZUL = (0, 0, 255)
COR_FUNDO = (54, 54, 54)
COR_TABULEIRO = (0, 31, 0)

# INICIANDO PROGRAMAÇÃO DO DISPLAY
display = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Jogo de Damas')
pygame.font.init()
clock = pygame.time.Clock()

# Classe principal

class Jogo:
	# Classe para tomar conta do status do jogo
	def __init__(self):
		self.status = 'jogando'
		self.turno = 1
		self.jogadores = ('x', 'o')
		self.cedula_selecionada = None
		self.pulando = False
		self.matriz_jogadores = [['x','-','x','-','x','-','x','-'],
							    ['-','x','-','x','-','x','-','x'],
				  			    ['x','-','x','-','x','-','x','-'],
							    ['-','-','-','-','-','-','-','-'],
							    ['-','-','-','-','-','-','-','-'],
							    ['-','o','-','o','-','o','-','o'],
							    ['o','-','o','-','o','-','o','-'],
							    ['-','o','-','o','-','o','-','o']]

	def avalia_clique(self, pos):
		if self.status == "jogando":
			linha, coluna = linha_clicada(pos), coluna_clicada(pos)
			if self.cedula_selecionada:
				movimento = self.is_movimento_valido(self.jogadores[self.turno % 2], self.cedula_selecionada, linha, coluna)
				if movimento[0]:
					self.jogar(self.jogadores[self.turno % 2], self.cedula_selecionada, linha, coluna, movimento[1])
				elif linha == self.cedula_selecionada[0] and coluna == self.cedula_selecionada[1]:
					movs = self.movimento_obrigatorio(self.cedula_selecionada)
					if movs[0] == []:
						if self.pulando:
							self.pulando = False
							self.proximo_turno()
					self.cedula_selecionada = None
			else:
				if self.matriz_jogadores[linha][coluna].lower() == self.jogadores[self.turno % 2]:
					self.cedula_selecionada = [linha, coluna]

	# VERIFICANDO SE UM MOVIMENTO REALIZADO PELO JOGADOR É VÁLIDO
	def is_movimento_valido(self, jogador, localizacao_cedula, linha_destino, coluna_destino):

		linha_originaria = localizacao_cedula[0]
		coluna_originaria = localizacao_cedula[1]

		obrigatorios = self.todos_obrigatorios()

		if obrigatorios != {}:
			if (linha_originaria, coluna_originaria) not in obrigatorios:
				return False, None
			elif [linha_destino, coluna_destino] not in obrigatorios[(linha_originaria, coluna_originaria)]:
				return False, None

		movimento, pulo = self.movimentos_possiveis(localizacao_cedula)

		if [linha_destino, coluna_destino] in movimento:
			if pulo:
				if len(pulo) == 1:
					return True, pulo[0]
				else:
					for i in range(len(pulo)):
						if abs(pulo[i][0] - linha_destino) == 1 and abs(pulo[i][1] - coluna_destino) == 1:
							return True, pulo[i]

			if self.pulando:
				return False, None

			return True, None

		return False, None

	# RETORNA TODOS OS MOVIMENTOS OBRIGATÓRIOS DE UM TURNO
	def todos_obrigatorios(self):
		todos = {}

		for r in range(len(self.matriz_jogadores)):
			for c in range(len(self.matriz_jogadores[r])):
				ob, pulos = self.movimento_obrigatorio((r, c))
				if  ob != []:
					todos[(r, c)] = ob

		return todos

	# RETORNA OS MOVIMENTOS OBRIGATÓRIOS DE UMA PEÇA QUE PODE SER JOGADA EM DETERMINADO TURNO
	def movimento_obrigatorio(self, localizacao_cedula):
		obrigatorios = []
		posicao_cedula_pulada = []

		l = localizacao_cedula[0]
		c = localizacao_cedula[1]

		jogador = self.jogadores[self.turno % 2]
		index = self.jogadores.index(jogador)

		array = [jogador.lower(), jogador.upper(), '-']

		if self.matriz_jogadores[l][c].islower() and self.matriz_jogadores[l][c] == jogador and \
		self.turno % 2 == index:
				if l > 0:
					if c < 7:
						if self.matriz_jogadores[l - 1][c + 1].lower() not in array:
							l_x = l - 1
							l_c = c + 1

							if l_x - 1 >= 0 and l_c + 1 <= 7:
								if self.matriz_jogadores[l_x - 1][l_c + 1] == '-':
									obrigatorios.append([l_x - 1, l_c + 1])
									posicao_cedula_pulada.append((l_x, l_c))
					if c > 0:
						if self.matriz_jogadores[l - 1][c - 1].lower() not in array:
							l_x = l - 1
							l_c = c - 1

							if l_x - 1 >= 0 and l_c - 1 >= 0:
								if self.matriz_jogadores[l_x - 1][l_c - 1] == '-':
									obrigatorios.append([l_x - 1, l_c - 1])
									posicao_cedula_pulada.append((l_x, l_c))
				if l < 7:
					if c < 7:
						if self.matriz_jogadores[l + 1][c + 1].lower() not in array:
							l_x = l + 1
							l_c = c + 1

							if l_x + 1 <= 7 and l_c + 1 <= 7:
								if self.matriz_jogadores[l_x + 1][l_c + 1] == '-':
									obrigatorios.append([l_x + 1, l_c + 1])
									posicao_cedula_pulada.append((l_x, l_c))
					if c > 0:
						if self.matriz_jogadores[l + 1][c - 1].lower() not in array:
							l_x = l + 1
							l_c = c - 1

							if l_x + 1 <= 7 and l_c - 1 >= 0:
								if self.matriz_jogadores[l_x + 1][l_c - 1] == '-':
									obrigatorios.append([l_x + 1, l_c - 1])
									posicao_cedula_pulada.append((l_x, l_c))

		elif self.matriz_jogadores[l][c].isupper() and self.matriz_jogadores[l][c] == jogador.upper() and \
		self.turno % 2 == index:
			conta_linha = l
			conta_coluna = c
			while True:
				if conta_linha - 1 < 0 or conta_coluna - 1 < 0: break
				else:
					if self.matriz_jogadores[conta_linha - 1][conta_coluna - 1] not in array:
						print 'chegou'
						l_x = conta_linha - 1
						l_c = conta_coluna - 1

						if l_x - 1 >= 0 and l_c - 1 >= 0:
							if self.matriz_jogadores[l_x - 1][l_c - 1] == '-':
								posicao_cedula_pulada.append((l_x, l_c))
								while True:
									if l_x - 1 < 0 or l_c - 1 < 0:
										break
									else:
										if self.matriz_jogadores[l_x - 1][l_c - 1] == '-':
											obrigatorios.append([l_x - 1, l_c - 1])
										else:
											break
									l_x -= 1
									l_c -= 1
						break
				conta_linha -= 1
				conta_coluna -= 1

			conta_linha = l
			conta_coluna = c
			while True:
				if conta_linha - 1 < 0 or conta_coluna + 1 > 7: break
				else:
					if self.matriz_jogadores[conta_linha - 1][conta_coluna + 1] not in array:
						l_x = conta_linha - 1
						l_c = conta_coluna + 1

						if l_x - 1 >= 0 and l_c + 1 <= 7:
							if self.matriz_jogadores[l_x - 1][l_c + 1] == '-':
								posicao_cedula_pulada.append((l_x, l_c))
								while True:
									if l_x - 1 < 0 or l_c + 1 > 7:
										break
									else:
										if self.matriz_jogadores[l_x -1][l_c + 1] == '-':
											obrigatorios.append([l_x - 1, l_c + 1])
										else:
											break
									l_x -= 1
									l_c += 1
						break
				conta_linha -= 1
				conta_coluna += 1

			conta_linha = l
			conta_coluna = c
			while True:
				if conta_linha + 1 > 7 or conta_coluna + 1 > 7: break
				else:
					if self.matriz_jogadores[conta_linha + 1][conta_coluna + 1] not in array:
						l_x = conta_linha + 1
						l_c = conta_coluna + 1

						if l_x + 1 <= 7 and l_c + 1 <= 7:
							if self.matriz_jogadores[l_x + 1][l_c + 1] == '-':
								posicao_cedula_pulada.append((l_x, l_c))
								while True:
									if l_x + 1 > 7 or l_c + 1 > 7:
										break
									else:
										if self.matriz_jogadores[l_x + 1][l_c + 1] == '-':
											obrigatorios.append([l_x + 1, l_c + 1])
										else:
											break
									l_x += 1
									l_c += 1
						break
				conta_linha += 1
				conta_coluna += 1

			conta_linha = l
			conta_coluna = c
			while True:
				if conta_linha + 1 > 7 or conta_coluna - 1 < 0: break
				else:
					if self.matriz_jogadores[conta_linha + 1][conta_coluna - 1] not in array:
						l_x = conta_linha + 1
						l_c = conta_coluna - 1

						if l_x + 1 <= 7 and l_c - 1 >= 0:
							if self.matriz_jogadores[l_x + 1][l_c - 1] == '-':
								posicao_cedula_pulada.append((l_x, l_c))
								while True:
									if l_x + 1 > 7 or l_c - 1 < 0:
										break
									else:
										if self.matriz_jogadores[l_x + 1][l_c - 1] == '-':
											obrigatorios.append([l_x + 1, l_c - 1])
										else:
											break
									l_x += 1
									l_c -= 1
						break
				conta_linha += 1
				conta_coluna -= 1

		return obrigatorios, posicao_cedula_pulada

	# MOSTRA OS MOVIMENTOS POSSÍVEIS DE UMA PEÇA SELECIONADA
	def movimentos_possiveis(self, localizacao_cedula):
		movimentos, pulos = self.movimento_obrigatorio(localizacao_cedula)

		if movimentos == []:
			linha_atual = localizacao_cedula[0]
			coluna_atual = localizacao_cedula[1]

			if self.matriz_jogadores[linha_atual][coluna_atual].islower():
				if self.matriz_jogadores[linha_atual][coluna_atual] == 'o':
					if linha_atual > 0:
						if coluna_atual < 7:
							if self.matriz_jogadores[linha_atual - 1][coluna_atual + 1] == '-':
								movimentos.append([linha_atual - 1, coluna_atual + 1])
						if coluna_atual > 0:
							if self.matriz_jogadores[linha_atual - 1][coluna_atual - 1] == '-':
								movimentos.append([linha_atual - 1, coluna_atual - 1])
				
				elif self.matriz_jogadores[linha_atual][coluna_atual] == 'x':
					if linha_atual < 7:
						if coluna_atual < 7:
							if self.matriz_jogadores[linha_atual + 1][coluna_atual + 1] == '-':
								movimentos.append([linha_atual + 1, coluna_atual + 1])
						if coluna_atual > 0:
							if self.matriz_jogadores[linha_atual + 1][coluna_atual - 1] == '-':
								movimentos.append([linha_atual + 1, coluna_atual - 1])
			elif self.matriz_jogadores[linha_atual][coluna_atual].isupper():
				conta_linha = linha_atual
				conta_coluna = coluna_atual
				while True:
					if conta_linha - 1 < 0 or conta_coluna - 1 < 0: break
					else:
						if self.matriz_jogadores[conta_linha - 1][conta_coluna - 1] == '-':
							movimentos.append([conta_linha - 1, conta_coluna - 1])
						else: break
					conta_linha -= 1
					conta_coluna -= 1

				conta_linha = linha_atual
				conta_coluna = coluna_atual
				while True:
					if conta_linha - 1 < 0 or conta_coluna + 1 > 7: break
					else:
						if self.matriz_jogadores[conta_linha - 1][conta_coluna + 1] == '-':
							movimentos.append([conta_linha - 1, conta_coluna + 1])
						else: break
					conta_linha -= 1
					conta_coluna += 1

				conta_linha = linha_atual
				conta_coluna = coluna_atual
				while True:
					if conta_linha + 1 > 7 or conta_coluna + 1 > 7: break
					else:
						if self.matriz_jogadores[conta_linha + 1][conta_coluna + 1] == '-':
							movimentos.append([conta_linha + 1, conta_coluna + 1])
						else: break
					conta_linha += 1
					conta_coluna += 1

				conta_linha = linha_atual
				conta_coluna = coluna_atual
				while True:
					if conta_linha + 1 > 7 or conta_coluna - 1 < 0: break
					else:
						if self.matriz_jogadores[conta_linha + 1][conta_coluna - 1] == '-':
							movimentos.append([conta_linha + 1, conta_coluna - 1])
						else: break
					conta_linha += 1
					conta_coluna -= 1
				
		return movimentos, pulos


	# EXECUTA UMA JOGADA
	def jogar(self, jogador, localizacao_cedula, linha_destino, coluna_destino, pulo):
		linha_atual = localizacao_cedula[0]
		coluna_atual = localizacao_cedula[1]
		char = self.matriz_jogadores[linha_atual][coluna_atual]
		self.matriz_jogadores[linha_destino][coluna_destino] = char
		self.matriz_jogadores[linha_atual][coluna_atual] = '-'
		if (jogador == 'x' and linha_destino == 7) or (jogador == 'o' and linha_destino == 0):
			self.matriz_jogadores[linha_destino][coluna_destino] = char.upper()
		if pulo:
			self.matriz_jogadores[pulo[0]][pulo[1]] = '-'
			self.cedula_selecionada = [linha_destino, coluna_destino]
			self.pulando = True
		else:
			self.cedula_selecionada = None
			self.proximo_turno()
		vencedor = self.verifica_vencedor()

		if vencedor != None:
			self.status = 'game over'

	# PRÓXIMO TURNO
	def proximo_turno(self):
		self.turno += 1

	# VERIFICA O VENCEDOR
	def verifica_vencedor(self):

		x = sum([contador.count('x') + contador.count('X') for contador in self.matriz_jogadores])
		o = sum([contador.count('o') + contador.count('O') for contador in self.matriz_jogadores])

		if (x == 0) or (x == 1 and not self.movimentos_possiveis(self.cedula_selecionada)[0]):
			if self.turno % 2 == 0:
				return 'o'


		if (o == 0) or (o == 1 and not self.movimentos_possiveis(self.cedula_selecionada)[0]):
			if self.turno % 2 == 1:
				return 'x'

		if x == 1 and o == 1:
			return 'empate'
		
		return None


	# DESENHAR TABULEIRO E PEÇAS
	def desenha(self):
		matriz = []

		for i in range(8):
			if i % 2 == 0:
				matriz.append(['#','-','#','-','#','-','#','-'])
			else:
				matriz.append(['-','#','-','#','-','#','-', '#'])

		y = 0
		for l in range(len(matriz)):
			x = 0
			for c in range(len(matriz[l])):
				if matriz[l][c] == '#':
					pygame.draw.rect(display, COR_TABULEIRO, (x, y, 75, 75))
				else:
					pygame.draw.rect(display, BRANCO, (x, y, 75, 75))
				x += 75
			y += 75

		if self.cedula_selecionada:
			obrigatorios = self.todos_obrigatorios()
			movs = self.movimentos_possiveis(self.cedula_selecionada)

			if obrigatorios != {}:
				if (self.cedula_selecionada[0], self.cedula_selecionada[1]) not in obrigatorios:
					x_vermelho = ALTURA / 8 * self.cedula_selecionada[1]
					y_vermelho = ALTURA / 8 * self.cedula_selecionada[0]

					pygame.draw.rect(display, VERMELHO_CLARO, (x_vermelho, y_vermelho, 75, 75))
				else:
					if movs[0] == []:
						x_vermelho = ALTURA / 8 * self.cedula_selecionada[1]
						y_vermelho = ALTURA / 8 * self.cedula_selecionada[0]

						pygame.draw.rect(display, VERMELHO_CLARO, (x_vermelho, y_vermelho, 75, 75))
					else:
						for i in range(len(movs[0])):
							x_possivel = ALTURA / 8 * movs[0][i][1]
							y_possivel = ALTURA / 8 * movs[0][i][0]

							pygame.draw.rect(display, VERDE_CLARO, (x_possivel, y_possivel, 75, 75))
			else:
				if self.pulando:
					x_vermelho = ALTURA / 8 * self.cedula_selecionada[1]
					y_vermelho = ALTURA / 8 * self.cedula_selecionada[0]

					pygame.draw.rect(display, VERMELHO_CLARO, (x_vermelho, y_vermelho, 75, 75))
				else:
					if movs[0] == []:
						x_vermelho = ALTURA / 8 * self.cedula_selecionada[1]
						y_vermelho = ALTURA / 8 * self.cedula_selecionada[0]

						pygame.draw.rect(display, VERMELHO_CLARO, (x_vermelho, y_vermelho, 75, 75))
					else:
						for i in range(len(movs[0])):
							x_possivel = ALTURA / 8 * movs[0][i][1]
							y_possivel = ALTURA / 8 * movs[0][i][0]

							pygame.draw.rect(display, VERDE_CLARO, (x_possivel, y_possivel, 75, 75))

		for l in range(len(self.matriz_jogadores)):
			for c in range(len(self.matriz_jogadores[l])):
				elemento = self.matriz_jogadores[l][c]
				if elemento != '-':
					x = ALTURA / 8 * c + ALTURA / 16
					y = ALTURA / 8 * l + ALTURA / 16

					if elemento.lower() == 'x':
						pygame.draw.circle(display, VERMELHO, (x, y), 20, 0)
						if elemento == 'X':
							pygame.draw.circle(display, PRETO, (x, y), 10, 0)
							pygame.draw.circle(display, AZUL, (x, y), 5, 0)
					else:
						pygame.draw.circle(display, BRANCO, (x, y), 20, 0)
						if elemento == 'O':
							pygame.draw.circle(display, PRETO, (x, y), 10, 0)
							pygame.draw.circle(display, AZUL, (x, y), 5, 0)

		fonte = pygame.font.Font(None, 20)
		x, o = 0, 0

		for i in self.matriz_jogadores:
			x += i.count('x')
			o += i.count('o')

		if self.status != 'game over':

			surface_texto, rect_texto = text_objects("Vermelho: " + str(12 - o), fonte, VERMELHO_CLARO)
			rect_texto.center = (650, 30)
			display.blit(surface_texto, rect_texto)

			surface_texto, rect_texto = text_objects("Branco: " + str(12 - x), fonte, BRANCO)
			rect_texto.center = (650, ALTURA - 30)
			display.blit(surface_texto, rect_texto)

			if self.turno % 2 == 1:
				surface_texto, rect_texto = text_objects("Turno do branco", fonte, BRANCO)
				rect_texto.center = (700, ALTURA / 2)
				display.blit(surface_texto, rect_texto)
			else:
				surface_texto, rect_texto = text_objects("Turno do vermelho", fonte, VERMELHO_CLARO)
				rect_texto.center = (700, ALTURA / 2)
				display.blit(surface_texto, rect_texto)
		else:
			surface_texto, rect_texto = text_objects("Game over", fonte, AZUL)
			rect_texto.center = (700, ALTURA / 3)
			display.blit(surface_texto, rect_texto)

# --- FUNÇÕES A SEREM UTILIZADAS  ---

# DEFINIR PADRÃO DE TEXTOS NA TELA
def text_objects(text, font, color):
	textSurface = font.render(text, True, color)
	return textSurface, textSurface.get_rect()

# FUNÇÃO PARA CRIAR UM BOTÃO
def cria_botao(msg, sqr, cor1, cor2, cor_texto, acao=None):
	mouse = pygame.mouse.get_pos()
	clique = pygame.mouse.get_pressed()

	if sqr[0] + sqr[2] > mouse[0] > sqr[0] and sqr[1] + sqr[3] > mouse[1] > sqr[1]:
		pygame.draw.rect(display, cor2, sqr)
		if clique[0] == 1 and acao != None:
			acao()
	else:
		pygame.draw.rect(display, cor1, sqr)

	fontePequena = pygame.font.SysFont('comicsansms', 20)
	surface_texto, rect_texto = text_objects(msg, fontePequena, cor_texto)
	rect_texto.center = (sqr[0] + 60, sqr[1] + 20)
	display.blit(surface_texto, rect_texto)

def creditos():
	sair = False
	while not sair:
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				pygame.quit()
				quit()
			if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
				sair = True

		display.fill(PRETO)
		fonte = pygame.font.SysFont('comicsansms', 20)
		surface_texto, rect_texto = text_objects("Programador: Lucas de Medeiros", fonte, BRANCO)
		rect_texto.center = ((LARGURA / 2), ALTURA / 3)
		display.blit(surface_texto, rect_texto)

		surface_texto, rect_texto = text_objects("Disciplina: Programacao 1 / Laboratorio de Programacao 1", fonte, BRANCO)
		rect_texto.center = ((LARGURA / 2), ALTURA / 2.7)
		display.blit(surface_texto, rect_texto)

		surface_texto, rect_texto = text_objects("Versao Python: 2.7.x", fonte, VERMELHO_CLARO)
		rect_texto.center = ((LARGURA / 2), ALTURA / 1.5)
		display.blit(surface_texto, rect_texto)

		surface_texto, rect_texto = text_objects("Versao Pygame: 1.9.1", fonte, VERMELHO_CLARO)
		rect_texto.center = ((LARGURA / 2), ALTURA / 1.3)
		display.blit(surface_texto, rect_texto)

		voltar = fonte.render('Pressione qualquer tecla para voltar ao menu.', False, VERDE_CLARO)
		display.blit(voltar, (25, 550))

		pygame.display.update()
		clock.tick(15)

def regras():
	sair = False

	while not sair:
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				sair = True
				pygame.quit()
				quit()
			if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
				sair = True

		display.fill(PRETO)

		fonte = pygame.font.SysFont('comicsansms', 20)

		info1 = fonte.render('O jogo de damas eh praticado em um tabuleiro de 64 casas.', False, (AZUL))
		info2 = fonte.render('O objetivo do jogo eh capturar todas as pecas do oponente.', False, (VERDE_ESCURO))
		info3 = fonte.render('A peca anda soh para frente, uma casa de cada vez, na diagonal.', False, (VERDE_ESCURO))
		info4 = fonte.render('Quando a peca atinge a oitava linha do tabuleiro ela vira dama.', False, (VERDE_ESCURO))
		info5 = fonte.render('A dama eh uma peca de movimentos mais amplos. Ela anda para frente e para tras,', False, (AZUL))
		info6 = fonte.render('quantas casas quiser, nao podendo saltar sobre uma peca da mesma cor. ', False, (AZUL))
		info7 = fonte.render('A captura e obrigatoria, ou seja, nao existe sopro.', False, (VERDE_ESCURO))
		info8 = fonte.render('Duas ou mais pecas juntas, na mesma diagonal, nao podem ser capturadas.', False, (VERDE_ESCURO))
		info9 = fonte.render('A peca e a dama podem capturar tanto para frente como para tras.', False, (AZUL))
		info10 = fonte.render('O movimento de captura pode ser encadeado sem que o jogador passe a vez.', False, (AZUL))
		
		game1 = fonte.render('Durante o jogo, ao clicar em uma peca, sera exibido em verde os movimentos', False, (VERMELHO))
		game2 = fonte.render('possiveis da mesma. Se nada acontecer ao clicar em uma peca, significa que', False, (VERMELHO))
		game3 = fonte.render('ela nao tem movimentos possiveis ou o turno pertence ao outro jogador.', False, (VERMELHO))

		voltar = fonte.render('Pressione qualquer tecla para voltar ao menu.', False, VERDE_CLARO)

		display.blit(info1, (5, 65))
		display.blit(info2, (5, 95))
		display.blit(info3, (5, 115))
		display.blit(info4, (5, 145))
		display.blit(info5, (5, 165))
		display.blit(info6, (5, 195))
		display.blit(info7, (5, 215))
		display.blit(info8, (5, 245))
		display.blit(info9, (5, 265))
		display.blit(info10, (5, 295))
		
		display.blit(game1, (5, 315))
		display.blit(game2, (5, 335))
		display.blit(game3, (5, 360))
		display.blit(voltar, (25, 550))

		pygame.display.update()
		clock.tick(60)

def tela_vencedor(vencedor):
	sair = False

	while not sair:
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				sair = True
				pygame.quit()
				quit()
			if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
				sair = True

		display.fill(PRETO)

		fonte = pygame.font.SysFont('comicsansms', 50)

		surface_texto, rect_texto = None, None

		if vencedor == "empate":
			surface_texto, rect_texto = text_objects("EMPATE!", fonte, BRANCO)
		elif vencedor == "x":
			surface_texto, rect_texto = text_objects("VITORIA DO  VERMELHO", fonte, VERMELHO)
		elif vencedor == "o":
			surface_texto, rect_texto = text_objects("VITORIA DO BRANCO", fonte, BRANCO)

		rect_texto.center = ((LARGURA / 2), ALTURA / 3)
		display.blit(surface_texto, rect_texto)

		fonte = pygame.font.Font(None, 30)
		voltar = fonte.render('Pressione qualquer tecla para voltar ao menu.', False, VERDE_CLARO)

		display.blit(voltar, (25, 550))

		pygame.display.update()
		clock.tick(60)

# TELA DO MENU
def menu_jogo():
	while True:
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				pygame.quit()
				quit()

		display.fill(PRETO)
		fonte = pygame.font.SysFont('comicsansms', 50)
		surface_texto, rect_texto = text_objects("Jogo de Damas", fonte, BRANCO)
		rect_texto.center = ((LARGURA / 2), ALTURA / 3)
		display.blit(surface_texto, rect_texto)

		cria_botao("INICIAR",(LARGURA - 760, ALTURA / 2, 120, 40), VERDE_CLARO, VERDE_ESCURO, BRANCO, loop_jogo)
		cria_botao("MANUAL",(LARGURA - 560, ALTURA / 2, 120, 40), BRANCO, CINZA, PRETO, regras)
		cria_botao("CREDITOS",(LARGURA - 360, ALTURA / 2, 120, 40), BRANCO, CINZA, PRETO, creditos)
		cria_botao("SAIR",(LARGURA - 160, ALTURA / 2, 120, 40), VERMELHO_CLARO, VERMELHO, BRANCO, sair)

		pygame.display.update()
		clock.tick(15)

# SAIR DO JOGO
def sair():
	pygame.quit()
	quit()

# FUNÇÕES AUXILIARES NO LOOP DO JOGO
def coluna_clicada(pos):
	x = pos[0]
	for i in range(1, 8):
		if x < i * ALTURA / 8:
			return i - 1
	return 7

def linha_clicada(pos):
	y = pos[1]
	for i in range(1, 8):
		if y < i * ALTURA / 8:
			return i - 1
	return 7

# LOOP DA TELA DO JOGO DE DAMAS
def loop_jogo():
	sair = False

	jogo = Jogo()

	while not sair:
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				sair = True
				pygame.quit()
				quit()
			if evento.type == pygame.MOUSEBUTTONDOWN:
				jogo.avalia_clique(pygame.mouse.get_pos())


		display.fill(PRETO)
		jogo.desenha()

		vencedor = jogo.verifica_vencedor()

		if vencedor is not None:
			sair = True
			tela_vencedor(vencedor)

		pygame.display.update()
		clock.tick(60)

menu_jogo()
pygame.quit()
quit()

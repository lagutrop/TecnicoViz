import fenixedu
import json
import os
import urllib.request
from urllib.error import HTTPError
import re
import requests 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import signal
from warnings import filterwarnings

try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
import tkinter
import time
import pymysql.cursors
import unicodedata
from difflib import SequenceMatcher

class User:
    username = ""
    password = ""

coursePairs = [
                ["Comunica��o de �udio e V�deo", "Comunica��o Multim�dia"],
                ["Modeliza��o de Sistemas Energ�ticos", "Modeliza��o e Economia de Sistemas Energ�ticos"],
                ["Pgp - Business Intelligence", "Pgp - Business Intelligence and Activity Monitoring"],
                ["Pgp - Estrat�gia e Sistemas de Informa��o", "Estrat�gia, Governa��o e Transforma��o Organizacional"],
                ["Pgp - Modela��o em Engenharia Empresarial", "Pgp - Engenharia Empresarial I"],
                ["Pgp - Teoria dos Sistemas e Modela��o Conceptual", "Pgp - Engenharia Empresarial II"],
                ["Pgp - Engenharia Empresarial e Integra��o de Sistemas de Informa��o", "Pgp - Engenharia Empresarial III"],
                ["Pgp - Gest�o de Projectos Inform�ticos", "Pgp - Gest�o de Projectos e Programas"],
                ["Pgp - Eengenharia Empresarial III", "Pgp - Engenharia Empresarial III"],
                ["Eco-Hidr�ulica e Modela��o em Sistemas Fluviais", "Ecohidr�ulica e Modela��o em Sistemas Fluviais"],
                ["T�picos Avan�ados em Fus�o Nuclear", "T�picos Avan�ados em F�sica dos Plasmas, Fus�o Nuclear e Lasers"],
                ["Estrutura e Comportamento dos Materiais de Constru��o", "Curso Avan�ado em Estrutura e Comportamento dos Materiais de Constru��o"],
                ["M�todos de Simula��o do Comportamento T�rmico e Ac�stico de Edif�cios", "Curso Avan�ado em Comportamento T�rmico e Ac�stico de Edif�cios"],
                ["Reabilita��o de Edif�cios e Estruturas Especiais: Estudos Avan�ados", "Curso Avan�ado em Reabilita��o de Edif�cios e Estruturas Especiais"],
                ["Estabilidade e Estruturas Met�licas ? Curso Avan�ado", "Curso Avan�ado em Estabilidade e Estruturas Met�licas"],
                ["Din�mica de Estruturas - Curso Avan�ado", "Curso Avan�ado em Din�mica de Estruturas"],
                ["Modela��o de Estruturas - Curso Avan�ado", "Curso Avan�ado em Modela��o de Estruturas"],
                ["Mec�nica Estat�stica e Transi��es de Fase.", "Mec�nica Estat�stica e Transi��es de Fase"],
                ["Teoria do Campo Avan�ada", "Teoria do Campo"],
                ["M�todos Computacionais", "M�todos Computacionais e Optimiza��o"],
                ["Sistemas de Comunica��o Via Sat�lite", "Sistemas de Comunica��o por Sat�lite"],
                ["Qualidade de Servi�o em Redes de Dados", "Qualidade de Servi�o em Redes de Dados por Pacotes"],
                ["T�picos Avan�ados em Arquitectura e Sistemas Distribu�dos", "T�picos Avan�ados em Arquitecturas e Sistemas Distribu�dos"],
                ["Engenharia de Ontologias e Sem�ntica de Redes", "Engenharia de Ontologias e Web Sem�ntica"],
                ["Semin�rio de Investiga��o em Matem�tica - Semestre 2", "Semin�rio de Investiga��o em Matem�tica"],
                ["Qu�mica de Interfaces/Superf�cies, Interfaces e Col�ides", "Superf�cies, Interfaces e Col�ides"],
                ["An�lise Num�rica Funcional e Optimiza��o", "An�lise Funcional Aplicada / An�lise Num�rica Funcional e Optimiza��o"],
                ["Modelos Matem�ticos em Hemodin�mica", "M�todos Matem�ticos em Hemodin�mica"],
                ["Modela��o e An�lise de Sistemas de Telecomunica��es por Fibra �ptica", "Sistemas Modernos de Telecomunica��es por Fibra �ptica"],
                ["Planeamento de Sistemas de Energia", "Gest�o e Planeamento de Sistemas de Energia"],
                ["Optimiza��o - Programa��o N�o Linear", "Optimiza��o N�o Linear", "Optimiza��o", "Optimiza��o N�olinear ", "Optimiza��o N�olinear"],
                ["Rob�tica Avan�ada", "T�picos Avan�ados em Rob�tica"],
                ["Projecto de Circuitos Integrados para R�dio Frequ�ncia", "Circuitos Integrados para R�dio Frequ�ncia"],
                ["Sistemas Din�micos de Eventos Discretos", "Sistemas de Eventos Discretos"],
                ["Projecto de Geradores El�ctricos de Baixa Velocidade para Aproveitamentos de Energias", "Projecto de Geradores El�ctricos de Baixa Velocidade para Aproveitamentos de Energias Renov�veis"],
                ["Processamento de Imagem e V�deo", "Processamento de Imagem e Video (Cmu)"],
                ["Instrumenta��o e Aquisi��o de Sinais", "Instrumenta��o e Aquisi��o de Sinais em Bioengenharia"],
                ["Complementos de An�lise Complexa", "An�lise Complexa"],
                ["An�lise Num�rica Funcional e Optimiza��o", "An�lise Funcional Aplicada", "An�lise Funcional Aplicada / An�lise Num�rica Funcional e Optimiza��o", "An�lise Funcional Aplicada"],
                ["Electr�nica e Instrumenta��o", "Sinais e Sistemas Mecatr�nicos"],
                ["Materiais e Processos de Constru��o", "Prospec��o Geofisica e Sondagens"],
                ["O Papel do Engenheiro", "Semin�rios de Engenharia de Materiais II"],
                ["Design e Materiais", "Design e Selec��o de Materiais"],
                ["Express�o Oral e Escrita-Materiais", "Semin�rios de Engenharia de Materiais I"],
                ["Sistemas de Informa��o e Bases de Dados / Bases de Dados", "Bases de Dados", "Bases de Dados/Sistemas de Informa��o e Bases de Dados"],
                ["Portfolio I", "Portfolio Pessoal I"],
                ["Digital Systems", "Sistemas Digitais", "Sistemas Digitais - 2� Fase", "Introdu��o � Arquitetura de Computadores"],
                ["Arquitectura de Computadores", "Arquitecturas de Computadores", "Organiza��o de Computadores"],
                ["Modela��o", "An�lise e Modela��o de Sistemas"],
                ["C�lculo Diferencial e Integral I - 2� Fase", "C�lculo Diferencial e Integral I", "C�lculo Diferencial e Integral I - 2� Fase - Alameda"],
                ["Teoria da Computa��o - 2� Fase", "Teoria da Computa��o"],
                ["�lgebra Linear", "�lgebra Linear - 2� Fase", " �lgebra Linear - 2� Fase - Alameda", "�lgebra Linear A"], 
                ["Fundamentos da Programa��o / Elementos de Programa��o - 2� Fase", "Fundamentos da Programa��o", "Elementos de Programa��o/Fundamentos de Programa��o/Programa��o", "Elementos de Programa��o/Fundamentos de Programa��o/Programa��o - 2� Fase", "Fundamentos da Programa��o/Programa��o", "Programa��o", "Elementos de Programa��o", "Fundamentos de Programa��o/Programa��o", "Fundamentos da Programa��o / Elementos de Programa��o", "Fundamentos da Programa��o - 2� Fase", 'Fundamentos de Programa��o'],
                ["Introdu��o aos Algoritmos e Estruturas de Dados / Algoritmos e Estrutura de Dados", "Introdu��o aos Algoritmos e Estruturas de Dados/Algoritmos e Estrutura de Dados", "Introdu��o aos Algoritmos e Estruturas de Dados", "Introdu��o aos Algoritmos e Estrutura de Dados", "Algoritmos e Estrutura de Dados"],
                ["Introdu��o � Interface Pessoa-M�quina", "Introdu��o �s Interfaces Pessoa-M�quina"],
                ["Teoria dos Circuitos e Fundamentos de Electr�nica", "Teoria dos Circuitos e Fund. de Electr�nica", "Introdu��o aos Circuitos e Sistemas Electr�nicos"],
                ["Introdu��o � Electr�nica das Comunica��es", "Electr�nica dos Sistemas Embebidos"],
                ["Redes Integradas de Comunica��es", "Arquitecturas de Redes"],
                ["Sinais e Sistemas", "Sistemas e Sinais"],
                ["Portfolio Pessoal II", "Portfolio II", "Comunica��o Oral e Escrita"],
                ["Gest�o de Redes e Servi�os", "Gest�o de Redes e Servi�os/Gest�o e Seguran�a de Redes", "Gest�o e Seguran�a de Redes / Gest�o de Redes e Servi�os", "Gest�o e Seguran�a de Redes"],
                ["Controlo", "Fundamentos de Controlo"],
                ["Instrumenta��o e Medidas", "Instrumenta��o e Aquisi��o de Sinais", "Instrumenta��o Electr�nica/Instrumenta��o e Medidas"],
                ["Electrotecnia e M�quinas El�ctricas", "Sistemas El�ctricos e Electromec�nicos", "Sistemas Electromec�nicos"],
                ["Programa��o de Sistemas", "Programa��o de Sistemas Computacionais"],
                ["Processos de Fabrico", "Electr�nica dos Sistemas Embebidos"],
                ["Direito", "Direito Empresarial"],
                ["Administra��o e Optimiza��o de Bases de Dados", "Administra��o de Dados e Sistemas de Informa��o"],
                ["Arquitectura Organizacional de Sistemas de Informa��o", "Fundamentos de Sistemas de Informa��o"],
                ["Tecnologia de Jogos e Simula��o", "Metodologia de Desenvolvimento de Jogos"],
                ["Arquitectura, Processos e Ferramentas de Sistemas de Informa��o", "Arquitetura Empresarial"],
                ["Gest�o e Administra��o de Sistemas e Redes", "Administra��o e Gest�o de Infraestruturas de It"],
                ["Programa��o 3D para Simula��o de Jogos", "Programa��o 3D"],
                ["Computa��o M�vel", "Computa��o M�vel e Ub�qua"],
                ["Gest�o e Tratamento de Informa��o", "An�lise e Integra��o de Dados"],
                ["Desenho e Desenvolvimento de Jogos", "Design de Jogos"],
                ["Sistemas Empresariais Integrados", "Integra��o Empresarial"],
                ["Plataformas para Aplica��es Distribu�das na Internet", "Desenvolvimento de Aplica��es Distribu�das"],
                ["Qualidade de Software", "Especifica��o de Software"],
                ["Portfolio III", "Portfolio Pessoal III"],
                ["Aplica��es e Implementa��es de Algoritmos Criptogr�ficos", "Aplica��es e Implementa��es de Algoritmos Criptogr�ficos / Aplica. Implementa��o de Sis. Seguran�a", "Aplica��es e Implementa��es de Algoritmos Criptogr�ficos / AI de Sistemas de Seguran�a"],
                ["Disserta��o de Mestrado em Engenharia Inform�tica e de Computadores", "Disserta��o - Mestrado em Engenharia Inform�tica e de Computadores"],
                ["Portfolio IV", "Portfolio Pessoal IV"],
                ["Plataformas para Desenvol. Aplica��es de Sist. Embebidos/Aplica��es para Sistemas Embebidos", "Plataformas para Desenvolvimento de Aplica��es para Sistemas Embebidos", "Aplica��es para Sistemas Embebidos"], 
                ["Ambientes Virtuais de Execu��o", "Computa��o em Nuvem e Virtualiza��o"],
                ["Recupera��o e Gest�o de Informa��o", "Processamento e Recupera��o de Informa��o"],
                ["Algoritmos e Optimiza��o", "Algoritmos e Optimiza��o / Optimiza��o e Algoritmos", "Optimiza��o e Algoritmos"],
                ["Controlo e Decis�o Inteligente", "Controlo e Decis�o Inteligente / Sistemas Inteligentes "],
                ["Processamento de Imagem e Vis�o", "Processamento de Imagem e Vis�o Artificial"],
                ["Sistemas Distribu�dos Tolerantes a Faltas", "Sistemas de Elevada Confiabilidade"],
                ["Instrumenta��o e Aquisi��o de Sinais", "Instrumenta��o e Aquisi��o de Sinais em Bioengenharia ", "Instrumenta��o e Aquisi��o de Sinais em Bioengenharia"],
                ["Processamento Digital de Sinais", "Processamento Digital de Sinais em Bioengenharia", "Processamento de Sinais em Bioengenharia"],
                ["Engenharia de C�lulas e Tecidos", "Eng� de C�lulas e Tecidos / Engenharia Celular"],
                ["Controlo e Opera��o de Sistemas de Energia", "Controlo e Optimiza��o de Sistemas de Energia"],
                ["Sistemas Computacionais", "Sistemas Computacionais Embebidos ", "Sistemas Computacionais Embebidos"],
                ["Sistemas de Energia em Ambientes de Mercado", "Mercados de Electricidade Competitivos"],
                [" Sistemas de Informa��o e Bases de Dados", "Sistemas de Informa��o e Bases de Dados / Bases de Dados", "Sistemas de Informa��o e Bases de Dados"],
                ["Microprocessadores", "Microcontroladores"],
                ["Oficinas", "Laborat�rio de Oficinas"],
                ["Laborat�rio de Investiga��o e Desenvolvimento", "Laborat�rio de Inova��o e Desenvolvimento"],
                ["Processos de Engenharia Qu�mica e Biol�gica I", "Processos de Engenharia Qu�mica e Biol�gica", " Processos de Engenharia Qu�mica e Biol�gica "],
                ["Portfolio em Engenharia Biol�gica", "Portfolio em Engenharia Biol�gica I"],
                ["Monitoriza��o e Controlo de Bioprocessos", "Supervis�o e Diagn�stico de Processos"],
                ["Planeamento Biof�sico", "Planeamento Biof�sico e Ordenamento do Territ�rio"],
                ["Electrodin�mica Espacial", "Ambiente Espacial"],
                ["Circuitos El�ctricos e Introdu��o � Electr�nica", "Teoria dos Circuitos e Fundamentos de Electr�nica"],
                ["Instrumenta��o", "Sensores e Sistemas"],
                [" Complementos de Tecnologia Mec�nica", "Complementos de Tecnologia Mec�nica"],
                ["Sistemas Inteligentes", "Controlo e Decis�o Inteligente / Sistemas Inteligentes "],
                ["Controlo Integrado da Produ��o / Modela��o e Controlo de Sistemas de Produ��o", "Controlo Integrado da Produ��o", "Controlo Integrado da Produ��o / RAAI", "Modela��o e Controlo de Sistemas de Manufactura", "Modela��o e Controlo de Sistemas de Manufactura / Modela��o e Controlo de Sistemas de Produ��o", " Modela��o e Controlo de Sistemas de Manufactura"],
                ["Hist�ria da Cidade", "Hist�ria da Cidade para Arquitectura"],
                ["Harmoniza��o F�sica/Desenho", "Harmoniza��o"],
                ["Projecto Final", "Projecto Final em Arquitectura 1 "],
                ["Disserta��o/Projecto Final em Arquitectura", "Disserta��o em Arquitectura"],
                ["Funda��es e Obras de Aterro", "Obras de Aterro"],
                ["Disserta��o de Mestrado em Engenharia Civil", "Disserta��o de Mestrado em Engenharia Civil - G"],
                ["Disserta��o de Mestrado em Engenharia Civil", "Disserta��o de Mestrado em Engenharia Civil - C"],
                ["Disserta��o de Mestrado em Engenharia Civil", "Disserta��o de Mestrado em Engenharia Civil - Uts"],
                ["Disserta��o de Mestrado em Engenharia Civil", "Disserta��o de Mestrado em Engenharia Civil - Hrh"],
                ["Disserta��o de Mestrado em Engenharia Civil", "Disserta��o de Mestrado em Engenharia Civil - e"],
                ["Transporte de Mercadorias e Processos Log�sticos", "Transporte de Mercadorias e Log�stica"],
                ["Estruturas Especiais e Funda��es", "Estruturas Especiais"],
                ["Constru��o e Manuten��o de Infra-Estruturas de Transportes", "Processos de Constru��o em Infraestruturas de Transportes", "Conserva��o de Infraestruturas de Transporte"],
                ["Gest�o de Empreendimentos e de Contratos", "Empreendimentos e Contratos"],
                ["Profissionalismo e �tica", "Profissionalismo e �tica / Forma��o Livre III"],
                ["Gest�o de Projectos I", "Gest�o de Projectos", "Gest�o de Projectos - Gest�o de Projectos de Engenharia"],
                [" Disserta��o de Mestrado em Engenharia e Gest�o Industrial", "Disserta��o de Mestrado em Engenharia e Gest�o Industrial", "Disserta��o em Engenharia e Gest�o Industrial"],
                ["An�lise e Gest�o do Risco em Projectos", "Avalia��o e Gest�o do Risco em Projectos"],
                ["Forma��o Livre III", "Profissionalismo e �tica / Forma��o Livre III"],
                ["Sistemas de Processamento Digital de Sinais", "Sistemas de Processamento Digital de Sinais / Processadores de Sinal para Comunica��es"],
                ["Op��o de Gest�o", "Op��o de Gest�o - 1�Sem."],
                ["Disserta��o de Mestrado em Engenharia Electr�nica", "Disserta��o - Mestrado em Engenharia Electr�nica"],
                ["Projecto em Engenharia de Redes de Comunica��es", "Projecto em Engenharia de Telecomunica��es e Inform�tica"],
                ["Disserta��o em Engenharia de Redes de Comunica��es", "Disserta��o em Engenharia de Telecomunica��es e Inform�tica"],
                ["Computa��o em Nuvem", "Computa��o em Nuvem e Virtualiza��o"],
                ["Monitoriza��o e Controlo", "Quimiometria, Monitoriza��o e Controlo"],
                ["Quimiometria-Mef", "Quimiometria, Monitoriza��o e Controlo"],
                ["Introdu��o �s Ci�ncias Farmac�uticas", "Ci�ncias Farmac�uticas"],
                ["Engenharia Farmac�utica Integrada", "Engenharia Farmac�utica"],
                ["Projecto/Disserta��o em Engenharia Farmac�utica", "Disserta��o"],
                ["Desenvolvimento de Medicamentos: Farmacocin�tica e Ensaios Cl�nicos", "Farmacocin�tica no Desenvolvimento de Medicamentos"],
                ["Projecto I ? Qu�mica Terap�utica", "Projecto I - Qu�mica Terap�utica"],
                ["Introdu��o �s Ci�ncias de Engenharia", "Ci�ncias de Engenharia Qu�mica"],
                ["Laborat�rios de Biotecnologia I", "Laborat�rios de Ci�ncias Biol�gicas"],
                ["Biotecnologia e Ambiente", "Biotecnologia Ambiental"],
                ["Projecto em Engenharia e Gest�o de Energia", "Projeto em Engenharia e Gest�o de Energia 1"],
                ["Avalia��o de Bens Imobili�rios e Manuten��o das Constru��es", "Avalia��o de Bens Imobili�rios"],
                ["Avalia��o de Bens Imobili�rios e Manuten��o das Constru��es", "Manuten��o das Constru��es"],
                ["Direito do Urbanismo e do Ambiente", "Direito do Urbanismo e do Ordenamento do Territ�rio"],
                ["Modelos Matem�ticos em Biomedecina", "Modelos Matem�ticos em Biomedicina"],
                ["Fundamentos de L�gica e Teoria da Computa��o(MMA)", "Fundamentos de L�gica e Teoria da Computa��o"],
                ["Introdu��o aos Processos Estoc�sticos(MMA)", "Introdu��o aos Processos Estoc�sticos"],
                ["Disserta��o de Mestrado", "Disserta��o de Mestrado em Matem�tica e Aplica��es"],
                ["Disserta��o/Projecto", "Disserta��o em Engenharia de Materiais"],
                ["Disserta��o/Projecto", "Projecto em Engenharia de Materiais"],
                ["Estabiliza��o de Maci�os Rochosos", "Geomec�nica Aplicada � Explora��o"],
                ["Disserta��o/Projecto em Eng� Geol�gica e de Minas", "Disserta��o em Engenharia Geol�gica e de Minas"],
                ["Disserta��o/Projecto em Eng� Geol�gica e de Minas", "Projecto em Engenharia Geol�gica e de Minas"],
                ["Disserta��o de Mestrado em Qu�mica", "Disserta��o de Mestrado em Qu�mica - A"],
                ["Micro e Nanofabrica��o", "T�cnicas de Micro e Nanofabrica��o"],
                ["Disserta��o de Mestrado em Bioengenharia e Nanossistemas", "Disserta��o de Bioengenharia e Nanossistemas", "Disserta��o em Bioengenharia e Nanossistemas"],
                ["Disserta��o de Mestrado em Bioengenharia e Nanossistemas", "Projecto em Bioengenharia e Nanossistemas"],
                ["Engenharia Celular", "Eng� de C�lulas e Tecidos / Engenharia Celular", "Engenharia de C�lulas e Tecidos"],
                ["Engenharia Biomolecular", "Engenharia Biomolecular e Celular"],
                ["Laborat�rios de Bioengenharia", "Laborat�rios de Bioengenharia e Nanossistemas"],
                ["Qu�mica de Interfaces", "Qu�mica de Interfaces/Superf�cies, Interfaces e Col�ides", "Superf�cies, Interfaces e Col�ides"],
                ["Disserta��o/Projecto - Mestrado em Engenharia e Arquitectura Naval", "Disserta��o em Engenharia e Arquitectura Naval"],
                ["Gest�o Urban�stica", "Gest�o Urban�stica e Economia do Imobili�rio/Gest�o Urban�stica"],
                ["Probabilidades e Estat�stica", "Introdu��o �s Probabilidades e Estat�stica", "Probabilidades e Estat�stica/Introdu��o �s Probabilidades e Estat�stica"],
                ["Disserta��o em Engenharia do Ambiente", "Disserta��o de Mestrado em Engenharia do Ambiente", "Disserta��o/Projecto em Engenharia do Ambiente"],
                ["Desenho e Modela��o Geom�trica I", "Desenho e Modela��o Geom�trica", "Desenho e Modela��o Geom�trica I / Desenho e Modela��o Geom�trica I"],
                ["Aspectos Profissionais e Sociais da Engenharia Inform�tica", "Computa��o e Sociedade"],
                ["An�lise e Simula��o Num�rica", "An�lise e Simula��o Num�rica / An�lise Num�rica II"],
                ["Ambientes e Impactes /  Ambiente Urbano e Espa�o Constru�do", "Ambiente Urbano e Espa�o Constru�do"],
                ["Introdu��o � Qu�mica-F�sica", "Introdu��o � Qu�mica-F�sica/Introdu��o � Qu�mica-F�sica/Qu�mica-F�sica de Materiais"],
                ["Probabilidades e Estat�stica", "Probabilidades e Estat�stica/Probabilidades Erros e Estat�stica", "Probabilidades e Estat�stica / Probabilidades e Estat�stica I"],
                ["Sistemas de Processamento Digital de Sinais /  Processadores de Sinal para Comunica��es", "Processadores de Sinal para Comunica��es"],
                ["Bases de Dados", "Bases de Dados/Sistemas de Informa��o e Bases de Dados"],
                ["Modelos Multicrit�rio de Apoio � Decis�o", "Avalia��o de Projectos e Decis�o P�blica / Modelos Multicrit�rio de Apoio � Decis�o", "Avalia��o de Projectos e Decis�o P�blica/Modelos Multicrit�rio de Apoio � Decis�o"],
                ["Elementos de Electrotecnia/Electrotecnia e M�quinas El�ctricas", "Elementos de Electrotecnia / Electrotecnia e M�quinas El�ctricas"],
                ["Gest�o da Produ��o II", "Gest�o da Produ��o e das Opera��es / Gest�o da Produ��o II", "Gest�o da Produ��o e das Opera��es/Gest�o da Produ��o II", "Gest�o da Produ��o e das Opera��es"],
                ["Gest�o Estrat�gica", "Gest�o Estrategica/Gest�o Estrat�gica e Comercial"],
                ["Infraestruturas Inst.e Projectos Industriais", "Infraestruturas Inst,e Projectos Industriais"],
                ["Agentes Aut�nomos e Sistemas Multiagente (SM)", "Agentes Aut�nomos e Sistemas Multi-Agente"],
                ["Gest�o de Redes e Sistemas Distribu�dos", "Gest�o de Redes e Sistemas Distribu�dos /  Gest�o de Redes e Servi�os", "Gest�o de Redes e Servi�os"],
                ["Sistemas de Apoio � Decis�o", "Sistemas de Apoio � Decis�o (SIE)"],
                ["Trabalho Final de Curso I", "Trabalho Final de Curso I (Leic)"],
                ["An�lise Matem�tica I - 2� Fase", "An�lise Matem�tica I", "An�lise Matem�tica I A"],
                ["An�lise Matem�tica II", "An�lise Matem�tica II A"],
                ["An�lise Matem�tica III", "An�lise Matem�tica III A"],
                ["An�lise Matem�tica IV", "An�lise Matem�tica IV A"],
                ["Arquitectura Tecnol�gica dos Sistemas de Informa��o", "Arquitectura Tecnol�gica de Sistemas de Informa��o Empresariais"],
                ["An�lise e S�ntese de Algoritmos", "An�lise e Sintese de Algoritmos"],
                ["Redes de Computadores", "Redes de Computadores I", "Redes de Computadores I / Redes de Computadores"],
                ["Sistemas Distribuidos", "Sistemas Distribu�dos"],
                ["Desenho T�cnico I", "Desenho T�cnico I/Desenho I"],
                ["Engenharia de Materiais/Materiais", "Engenharia de Materiais"],
                ["Fundamentos de Gest�o", "Fundamentos de Gestao", "Fundamentos de Gestao/Economia II"],
                ["F�sica II/Electro. e �ptica/Termo. e Est. da Mat�ria", "Termodin�mica e Estrutura da Mat�ria"],
                ["M�quinas e Sistemas Mar�timos II", "M�quinas e Sistemas Mar�timos II/M�quinas e Sistemas Mar�timos III"],
                ["Qu�mica/Qu�mica Geral", "Qu�mica Geral", "Qu�mica"],
                ["Hidr�ulica", "Hidr�ulica/Mec�nica dos Fluidos e Hidr�ulica"],
                ["Introdu��o � Investiga��o em Engenharia Electrot�cnica e de Computadores", "Introdu��o � Investiga��o e ao Projecto em Engenharia Electrot�cnica e de Computadore"],
                ["Design of Robust Multivariable Feedback Control Systems" , "Design of Robust Multivariable Feedback Control Systems MD"],
                ["Dynamic Stochastic Estimation, Prediction and Smoothing", "Dynamic Stochastic Estimation, Prediction and Smoothing MD"],
                ["An�lise de Sistemas Aplicada � Gest�o Costeira", "An�lise de Sistemas Aplicada � Gest�o Costeira"],
                ["Gest�o e Ordenamento de Recursos Litorais", "Gest�o e Ordenamento de Sistemas Litorais"],
                ["Modela��o de Fen�menos de Transportes e da Qualidade da �gua", "Modela��o de Fen�menos de Transporte e da Qualidade da �gua"],
                ["Introdu��o a Metodologias de Investiga��o S�cio-Econ�mica", "Introdu��o a Metodologias de Investiga��o Socio-Econ�mica"],
                ["Aspectos de Qu�mica de Elementos e Compostos no Ambiente. Toxicidade e Polui��o", "Aspectos de Quimica de Elementos e Compostos no Ambiente. Toxicidade e Polui��o", "Aspectos da Qu�mica de Produtos Naturais, Poluentes e Toxicologia"],
                ["Ensaios Espec�ficos e Imunol�gicos em An�lise Qu�mica", "Ensaios Espec�ficos e Imunol�gicos em An�lise Qu�mica. An�lise Sensorial"],
                ["Economia e Planeamento dos Eventos e Atrac��es Tur�sticas", "Economia e Planeamento dos Eventos e Atrac��es Turisticas"],
                ["Diagn�stico e Conserva��o de Estradas e Obras de Arte" , "Diagn�stico e Manuten��o de Estradas e Obras de Arte"],
                ["Projectos de Infraestruturas Urbanas I", "Projecto de Infraestruturas Urbanas I"],
                ["Estudos de Ci�ncia:Arte,Tecnologia e Sociedade", "Estudos de Ci�ncia: Arte, Tecnologia e Sociedade"],
                ["Estudos de Impacto Ambiental/Impactes Ambientais", "Estudos de Impacto Ambiental", "Impactes Ambientais", "Ambientes e Impactes", "Ambientes e Impactes /  Ambiente Urbano e Espa�o Constru�do"],
                ["Introdu��o � Arquitectura e ao Projecto", "Introdu��o � Arquitectura"],
                ["Reabilita��o de Constru��es - Estudo de Casos", "Reabilita��o de Constru��es- Estudo de Casos", "Reabilita��o de Constru��es. Estudos de Caso"],
                ["Tecnologias de Instala��es e Equipamentos Prediais" , "Tecnologia de Instala��es e Equipamentos Prediais"],
                ["Elementos de Criptografia", "Criptografia e Protocolos de Seguran�a", "Elementos de Criptografia /  Criptografia e Protocolos de Seguran�a"],
                ["Desenho", "Desenho I"],
                ["Disserta��o de Mestrado em Eng� F�sica Tecnol�gica", "Disserta��o de Mestrado em Engenharia F�sica Tecnol�gica"],
                ["Economia do Ambiente", "Economia do Ambiente / Economia, Energia e Ambiente"],
                ["Sistemas de Informa��o Geogr�fica e Bases de Dados", "Sistemas de Informa��o Geogr�fica"],
                ["Laborat�rio de Qu�mica Geral I", "Laborat�rio de Qu�mica Geral"],
                ["Monitoriza��o e Controlo de Bioprocessos", "Monitoriza��o e Controlo de Bio Processos"],
                ["Qu�mica Bioinorg�nica", "Qu�mica Bio Inorg�nica"],
                ["Qu�mica-F�sica", "Qu�mica-F�sica I", " Qu�mica-F�sica / Qu�mica-F�sica I", "Qu�mica F�sica"],
                ["Instala��es,Servi�os Industriais e Seguran�a", "Instala��es, Servi�os Industriais e Seguran�a"],
                ["Bioqu�mica e Biologia Molecular", "Biologia Celular e Molecular/Bioquimica e Biologia Molecular"],
                ["Fisiologia de Sistemas" , "Fisiologia de Sistemas I"],
                ["Din�mica das Rochas/Din�mica dos Solos e das Rochas", "Din�mica dos Solos e Rochas", "Din�mica das Rochas"],
                ["Urban�stica ? Hist�ria e Teorias da Cidade", "Urban�stica, Hist�ria e Teorias da Cidade"]
              ]   

degreePairs = {
    "A-pB" : "A",
    "EA-pB" : "EAer",
    "EBL-pB" : "EBiol",
    "EBM-pB" : "EBiom",
    "EC-pB" : "EC",
    "EMAT-pB" : "EMat",
    "ERCI-pB" : "ERC",
    "EAM-pB" : "EAmbi",
    "ET-pB" : "ET",
    "EN-pB" : "EAN",
    "EGI-pB" : "EGI",
    "EE-pB" : "EE",
    "EEC-pB" : "EEC",
    "EFT-pB" : "EFT",
    "EGM-pB" : "EGM",
    "EIC-pB" : "EIC-A",
    "EIC-Taguspark-pB" : "EIC-T",
    "EM-pB" : "EMec",
    "EQ-pB" : "EQ",
    "MAC-pB" : "MAC",
    "Q-pB" : "Q"
}
        
def fenixEduDataRetrieval():
    # Create the configuration object with clien_id and client_secret
    config = fenixedu.FenixEduConfiguration.fromConfigFile('fenixedu.ini')
    
    # Connect to the fenixedu api
    client = fenixedu.FenixEduClient(config)
    
    #Create \json directory if doesn't exist
    path = os.getcwd() + "\\json"
    if not os.path.exists(path):
        os.makedirs(path)
   
    #Create \degrees directory if doesn't exist
    if not os.path.exists(path + "\\degrees"):
        os.makedirs(path + "\\degrees")    

    # Get all the degrees and write to json file
    getDegrees(client)
    
    # Get all the academic terms and write to json file
    getAcademicTerms(client)
    
    # Get all the courses and write to json file
    getDegreeCourses(client)
        
def getDegrees(client):
    # Load academic terms json file
    termsFile = open(os.getcwd() + "\\json\\academicTerms.json", "r")
    termsList = json.load(termsFile)
    for key in termsList:
        url = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/degrees?academicTerm=" + key
        try:
            pageRetrieved = urllib.request.urlopen(url).read()
        except:
            time.sleep(500)    
            pageRetrieved = urllib.request.urlopen(url).read()
        degrees = json.loads(pageRetrieved.decode('utf-8'))            
        # Ignore years without data
        if len(degrees) != 0:
            newKey = key.replace("/", " ")
            path = os.getcwd() + "\\json\\degrees" + newKey + ".json"
            degreesJson = open(path, "w", encoding = 'utf-8')
            json.dump(degrees, degreesJson, sort_keys = True, ensure_ascii = False, indent = 4)        
        
def getAcademicTerms(client):
    path = os.getcwd() + "\\json\\academicTerms.json"
    if not os.path.isfile(path):
        terms = client.get_academic_terms()
        termsJson = open(path, "w")
        json.dump(terms, termsJson, sort_keys = True, ensure_ascii = False, indent = 4)
    
def getDegreeCourses(client):
       
    # Load academic terms json file
    termsFile = open(os.getcwd() + "\\json\\academicTerms.json", "r")
    termsList = json.load(termsFile)
    # Build UI
    u = User()
    buildUI(u)
    
    for key in termsList:
        newKey = key.replace("/", " ")
        path = os.getcwd() + "\\json\\degrees"      
        currentYear = key.split('/',1)[0]
        # Load degrees json file
        if not os.path.isfile(path + newKey + ".json") or int(currentYear) < 2001:
            continue
        degreesFile = open(path + newKey + ".json", "r", encoding="utf-8")
        degreesList = json.load(degreesFile)        
        for i in range(0, len(degreesList)):
            # Create directory for each degree if they don't exist
            degreeName = degreesList[i]["name"]
            degreeType = degreesList[i]["type"]
            degreeAcronym = degreesList[i]["acronym"]
            degreeId = degreesList[i]["id"]
            degreeTypeParsed = degreeType.split(' Bolonha',1)[0]
            degreePath = path + "\\" + degreeAcronym
            if not os.path.exists(degreePath):
                os.makedirs(degreePath)
            # Extract all degrees from the web API
            if key == "2006/2007":
                url = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/degrees/" + degreesList[i]["id"] + "/courses?academicTerm=1%20Semestre%20" + key
                url1 = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/degrees/" + degreesList[i]["id"] + "/courses?academicTerm=2%20Semestre%20" + key
                try:
                    pageRetrieved = urllib.request.urlopen(url).read()
                    pageRetrieved1 = urllib.request.urlopen(url1).read()
                except:
                    #time.sleep(500)    
                    pageRetrieved = urllib.request.urlopen(url).read() 
                    pageRetrieved1 = urllib.request.urlopen(url1).read()
                courses = json.loads(pageRetrieved.decode('utf-8'))
                courses1 = json.loads(pageRetrieved1.decode('utf-8'))
                courses.extend(courses1)
            else: 
                url = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/degrees/" + degreesList[i]["id"] + "/courses?academicTerm=" + key
                try:
                    pageRetrieved = urllib.request.urlopen(url).read()
                except:
                    time.sleep(500)    
                    pageRetrieved = urllib.request.urlopen(url).read()
                courses = json.loads(pageRetrieved.decode('utf-8'))            
            # Ignore years without data
            if len(courses) != 0:
                coursesJson = open(degreePath + "\\" + degreeName.lower() + " " + newKey + ".json", "w", encoding="utf-8")
                json.dump(courses, coursesJson, sort_keys = True, ensure_ascii = False, indent = 4)                
                # Extract courses from all the degrees
                for j in range(0, len(courses)):
                    isInLog = False
                    courseId = courses[j]["id"]
                    # Acronym instead of name because some courses have big length
                    courseName = courses[j]["acronym"] 
                    if 'FLTP-' in courseName:
                        courseName = 'FLTP'
                    # Check log file to see if the course was already loaded
                    courseLog = degreeAcronym + " " + courseName + " " + courseId + " " + newKey + "\n"
                    if not os.path.isfile(os.getcwd() + '\\' "logFile.txt"):                    
                        file = open(os.getcwd() + '\\' "logFile.txt","w")
                        file.close()
                    readFile = open(os.getcwd() + '\\' "logFile.txt","r")                    
                    for line in readFile:
                        if courseLog == line:
                            isInLog = True
                            break
                        else:
                            isInLog = False
                    readFile.seek(0)
                    readFile.close()
                    if isInLog == False:                  
                        # Load individual courses' info
                        try:
                            individualCourse = client.get_course(courseId)
                        except:
                            time.sleep(240)
                            individualCourse = client.get_course(courseId)
                        # Load course evaluations (exams and tests dates)
                        courseEvaluation = client.get_course_evaluations(courseId)
                        # Load course groups (number of elements, capacity)
                        courseGroups = client.get_course_groups(courseId)
                        # Load course schedule (class hour, location, time spent)
                        courseSchedule = client.get_course_schedule(courseId)
                        # Load students in a specific course
                        courseStudents = client.get_course_students(courseId)
                        coursePath = degreePath + "\\" + courseName + " " + courseId
                        if not os.path.exists(coursePath):
                            os.makedirs(coursePath)
                        evaluationPath = coursePath + "\\" + "evaluations"
                        groupsPath = coursePath + "\\" + "groups"
                        schedulePath = coursePath + "\\" + "schedule"
                        studentsPath = coursePath + "\\" + "students"
                        qucPath = coursePath + "\\" + "quc"
                        # Create the necessary folders
                        if not os.path.exists(evaluationPath):
                            os.makedirs(evaluationPath)
                        if not os.path.exists(groupsPath):
                            os.makedirs(groupsPath)                            
                        if not os.path.exists(schedulePath):
                            os.makedirs(schedulePath)
                        if not os.path.exists(studentsPath):
                            os.makedirs(studentsPath)
                        if not os.path.exists(qucPath):
                            os.makedirs(qucPath)
                        url = individualCourse['url']
                        if not url == "":
                            if 'semestre' in url:
                                url = url.split("semestre", 1)[0]
                                url = url + "semestre"    
                            login = "https://id.tecnico.ulisboa.pt/cas/login"  
                            headers = { 'Accept':'*/*',
                                        'Accept-Encoding':'gzip, deflate, sdch',
                                        'Content-Type':'text/html;charset=UTF-8',
                                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
                                    }
                            for pos, value in enumerate(headers):
                                webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(pos)] = value
                            browser = webdriver.PhantomJS(os.getcwd()+'\\phantomjs.exe', service_args=['--ignore-ssl-errors=true'])                     
                            browser.maximize_window()
                            try:
                                url = unicodedata.normalize('NFKD', url).encode('ASCII','ignore').decode('utf-8')
                                if '~' in url:
                                    with urllib.request.urlopen(url) as response:
                                        pageRetrieved2 = response.read().decode('latin-1')                                    
                                else:
                                    with urllib.request.urlopen(url) as response:
                                        pageRetrieved2 = response.read().decode('utf-8')
                            except urllib.error.HTTPError as err:
                                if err.code == 404:
                                    # Save individual course information in json file
                                    writeToFile(coursePath, courseName.lower(), newKey, individualCourse)
                                    # Save evaluation information in json file
                                    writeToFile(evaluationPath, "evaluation", newKey, courseEvaluation)
                                    # Save groups information in json file
                                    writeToFile(groupsPath, "groups", newKey, courseGroups)
                                    # Save schedule information in json file
                                    writeToFile(schedulePath, "schedule", newKey, courseSchedule) 
                                    # Save students information in json file
                                    writeToFile(studentsPath, "students", newKey, courseStudents)
                                    # Save log information
                                    file = open(os.getcwd() + '\\' "logFile.txt","a")
                                    file.write(courseLog)                                      
                                    file.close()
                                    continue
                                else:
                                        time.sleep(500)
                                        if '~' in url:
                                            with urllib.request.urlopen(url) as response:
                                                pageRetrieved2 = response.read().decode('latin-1')         
                                        else:
                                            with urllib.request.urlopen(url) as response:
                                                pageRetrieved2 = response.read().decode('utf-8')
                            pageRetrieved2 = re.findall(r'<a class="item"(.*?)</a>',pageRetrieved2,re.DOTALL)
                            for text in pageRetrieved2:
                                if 'Resultados QUC' in text:                                        
                                    resultados = text
                                    url = re.findall(r'="(.*?)">',resultados,re.DOTALL)
                                    browser.get(url[0])
                                    qucPage = browser.page_source
                                    if 'caracter p�blico' in qucPage:
                                        browser.get(login)
                                        try:
                                            username = browser.find_element_by_name("username")
                                        except:
                                            time.sleep(500)
                                            browser.get(login)
                                            username = browser.find_element_by_name("username")
                                        try:
                                            password = browser.find_element_by_name("password")
                                        except:
                                            time.sleep(500)
                                            browser.get(login)
                                            password = browser.find_element_by_name("password")                                    
                                        username.send_keys(u.username)
                                        password.send_keys(u.password)                                    
                                        browser.find_element_by_name("submit-istid").click()
                                        browser.get('https://fenix.tecnico.ulisboa.pt/login.do')
                                        browser.get(url[0])
                                        qucPage = browser.page_source                                  
                                    links = browser.find_elements_by_xpath("//a[contains(@href,'publico/view')]")
                                    window = 1
                                    for link in links:
                                        browser.switch_to_window(browser.window_handles[0])
                                        webDegreeAcronym = re.findall(r'\((.*?)\)',link.text,re.DOTALL)
                                        if not webDegreeAcronym:
                                            webDegreeAcronym = []
                                            webDegreeAcronym.append("")
                                        link.click()
                                        browser.switch_to_window(browser.window_handles[window])
                                        page = browser.page_source
                                        window+=1
                                        if "Ocorreu um erro" not in page:
                                            approvals, parsedPage = parseQucTable(page)
                                            evaluationType = "Avalia��o dos QUC\n"
                                            if 'Docente:' in page:
                                                beautifulSoupPage = BeautifulSoup(page, "html.parser")
                                                teacher = beautifulSoupPage.body.find_all('p')
                                                for tag in teacher:
                                                    if 'Docente:' in str(tag):
                                                        teacherName = re.findall(r'<b>(.*?)</b>',str(tag),re.DOTALL)
                                                qucFile = open(qucPath + "\\" + "quc" + " " + newKey + ".txt", "a", encoding="utf-8")
                                                evaluationType = "Avalia��o dos QUC do professor " + teacherName[0] + "\n"
                                            else:
                                                if webDegreeAcronym[0] not in degreeAcronym:
                                                    continue                                                
                                                qucFile = open(qucPath + "\\" + "quc" + " " + newKey + ".txt", "w", encoding="utf-8")
                                                for row in approvals:
                                                    qucFile = open(qucPath + "\\" + "quc" + " " + newKey + ".txt", "a", encoding="utf-8")
                                                    if 'Taxa de aprova��o' in row:    
                                                        parseQucInfo(qucFile, "Taxa de aprova��o\n", row)
                                                    if 'M�dia classifica��es' in row:
                                                        parseQucInfo(qucFile, "M�dia das notas dos alunos\n", row)
                                            if parsedPage:
                                                qucFile.write(evaluationType)
                                                parseQucEvaluationInfo(qucFile, parsedPage)
                                            if 'e Tipo de aula:' in page:
                                                teacherEvaluation = re.findall(r'e Tipo de aula:(.*?)</div>',page,re.DOTALL)
                                                teacherEvaluation = teacherEvaluation[0].replace('\n', '')
                                                teacherEvaluation = teacherEvaluation.replace('\t', '')
                                                qucFile.write("Avalia��o do professor " + teacherName[0] + "\n")
                                                qucFile.write("%s\n" % teacherEvaluation)
                                            qucFile.close()

                            browser.service.process.send_signal(signal.SIGTERM)                                            
                            browser.quit()
                        # Save individual course information in json file
                        writeToFile(coursePath, courseName.lower(), newKey, individualCourse)
                        # Save evaluation information in json file
                        writeToFile(evaluationPath, "evaluation", newKey, courseEvaluation)
                        # Save groups information in json file
                        writeToFile(groupsPath, "groups", newKey, courseGroups)
                        # Save schedule information in json file
                        writeToFile(schedulePath, "schedule", newKey, courseSchedule) 
                        # Save students information in json file
                        writeToFile(studentsPath, "students", newKey, courseStudents)
                        # Save log information
                        file = open(os.getcwd() + '\\' "logFile.txt","a")
                        file.write(courseLog)                                      
                        file.close()

def buildUI(u):
    guiWindow = tkinter.Tk()
    guiWindow.title("T�cnicoVis Login")
    guiWindow.geometry("270x210")
    guiWindow.configure(bg="#7fc6db")  
    def procede(event=None):
        u.username = user.get()
        u.password = passw.get()
        guiWindow.destroy()    
    title1 = tkinter.Label(guiWindow, text="--Log in with your istId--\n", bg="#7fc6db")
    usertitle = tkinter.Label(guiWindow, text="---Username---", bg="#7fc6db")
    passtitle = tkinter.Label(guiWindow, text="---Password---", bg="#7fc6db")    
    user = tkinter.Entry(guiWindow)
    passw = tkinter.Entry(guiWindow, show='*')    
    go = tkinter.Button(guiWindow, text="Log in", command=procede, bg="#40b7b3")
    title1.pack()
    usertitle.pack()
    user.pack()
    passtitle.pack()
    passw.pack()
    go.pack()
    guiWindow.attributes("-topmost", True)    
    guiWindow.lift()
    guiWindow.bind('<Return>', procede)
    guiWindow.mainloop()    

def writeToFile(path, folder, year, data):
    jsonFile = open(path + "\\" + folder + " " + year + ".json", "w", encoding="utf-8")
    json.dump(data, jsonFile, sort_keys = True, ensure_ascii = False, indent = 4) 
    
def parseQucInfo(file, text, row):
    file.write(text)
    info = re.findall(r'<td>(.*?)</td>',row,re.DOTALL)
    info = info[0].replace('\n', '')
    info = info.replace('\t', '')
    file.write("%s\n" % info)
    
def parseQucEvaluationInfo(file, page):
    for position in page:
        if '<b>' in str(position) or '-' in str(position):
            position = str(position).replace('<td class="x1">', '')
            position = position.replace('<td class="x2">', '')
            position = position.replace('<td class="x3">', '')
            position = position.replace('<b>', '')
            position = position.replace('</b>', '')
            position = position.replace('\n', '')
            position = position.replace(' ', '')
            position = position.replace('</td>', '')            
            file.write("%s\n" % position)
            
def parseQucTable(page):
    beautifulSoupPage = BeautifulSoup(page, "html.parser")
    parsedPage = beautifulSoupPage.body.find_all('td', attrs={'class':["x2", "x1", "x3"]})
    approvals = beautifulSoupPage.body.find('table', attrs={'class':'graph-2col'})
    approvals = re.findall(r'<tr>(.*?)</tr>',str(approvals),re.DOTALL)
    return approvals, parsedPage

def findPath(degreeName, degreeAcronym, path, newYear):
    coursePath = path + "\\" + degreeAcronym + "\\" + degreeName.lower() + " " + newYear + ".json"   
    splittedDegreeName = degreeName
    return splittedDegreeName, coursePath
        
        
def approvalsCalculation():
    termsFile = open(os.getcwd() + "\\json\\academicTerms.json", "r")
    termsList = json.load(termsFile)     
    path = os.getcwd() + "\\json\\degrees"
    # Load academic terms json file
    for key in termsList:
        newKey, year = getYear(key) 
        currentYear = key.split('/',1)[0]
        afterYear = int(currentYear)+1
        nextYear = str(int(year) + 1) + ' ' + str(int(year) + 2)    
        if not os.path.isfile(path + newKey + ".json"):
            continue
        with open(path + newKey + ".json", encoding="utf8") as degreesFile:
            degreesList = json.load(degreesFile)        
        for i in range(0, len(degreesList)):
            degreeName, degreeId, degreeTypeParsed, degreeAcronym, degreePath = getDegree(degreesList[i], path)
            coursesListPath = degreePath + "\\" + degreeName.lower() + " " + newKey + ".json"
            # Licenciaturas e mestrados
            if not os.path.isfile(coursesListPath) or 'Diploma' in degreeTypeParsed:
                continue
            with open(coursesListPath, encoding="utf8") as coursesFile:
                courseList = json.load(coursesFile)
            for j in range(0, len(courseList)):
                courseName, courseFullName, courseTerm, courseId, coursePath, courseCredits = getCourse(courseList[j], degreePath, key)
                courseFullName = courseFullName.split(' (', 1)[0].split('(', 1)[0]
                reproval = 0
                studentsPath = degreePath + "\\" + courseName + " " + courseId + "\\" + "students" + "\\" + "students " + newKey + ".json"
                if not os.path.isfile(studentsPath):
                    continue 
                with open(studentsPath, encoding="utf8") as studentsFile:
                    studentsList = json.load(studentsFile)
                studentsNumber = 0
                # Detect end of courses
                courseEnded = True
                checkedCourses = 0
                parsedDegreeAcronym = degreeAcronym[1:]
                for student in studentsList["students"]:
                    studentId = student["username"]
                    studentDegree = student["degree"]["acronym"]
                    studentDegree = studentDegree[1:]  
                    # Count students of that course in specific degree
                    if getDegreePairs(parsedDegreeAcronym, studentDegree):
                        studentsNumber += 1                    
                    else:
                        continue
                    def doLoop():
                        degreePath = path + "\\" + degreeAcronym
                        nonlocal checkedCourses
                        nonlocal courseEnded
                        for w in termsList:
                            nextYears = w.split('/',1)[0] 
                            if int(nextYears) >= int(currentYear):
                                newYear = w.replace("/", " ")
                                splittedDegreeName, coursePath = findPath(degreeName, degreeAcronym, path, newYear)
                                if not os.path.isfile(coursePath):   
                                    try:
                                        splittedDegreeName, coursePath = findPath(degreeName.lower().split('ci�ncias de engenharia - ', 1)[1], degreeAcronym, path, newYear)
                                    except IndexError:
                                        splittedDegreeName, coursePath = findPath(degreeName, degreeAcronym.split('-pB', 1)[0], path, newYear)
                                if not os.path.isfile(coursePath):       
                                    try:
                                        splittedDegreeName, coursePath = findPath(degreeName.lower().split('ci�ncias de engenharia - ', 1)[1], degreeAcronym.split('-pB', 1)[0], path, newYear)
                                    except IndexError:
                                        pass            
                                if not os.path.isfile(coursePath):
                                    continue 
                                with open(coursePath, encoding="utf8") as courseCompareFile:
                                    courseCompareList = json.load(courseCompareFile)
                                for similarCourse in range(0, len(courseCompareList)):
                                    courseCompareName = courseCompareList[similarCourse]["name"]
                                    courseCompareId = courseCompareList[similarCourse]["id"]
                                    courseCompareTerm = courseCompareList[similarCourse]["academicTerm"]
                                    courseCompareTerm = courseCompareTerm.replace('Semestre ' + w, '')
                                    courseCompareTerm = courseCompareTerm.replace('�', '')
                                    courseCompareAcronym = courseCompareList[similarCourse]["acronym"]
                                    courseComparePath = degreePath + '\\' + courseCompareAcronym + ' ' + courseCompareId + '\\' + courseCompareAcronym.lower() + " " + newYear + ".json"
                                    if not os.path.isfile(courseComparePath):
                                        continue   
                                    if getCoursePairs(courseFullName, courseCompareName): 
                                        if int(nextYears) > int(currentYear) or (int(courseCompareTerm) > int(courseTerm) and int(nextYears) == int(currentYear)):                                            
                                            studentsComparePath = degreePath + "\\" + courseCompareAcronym + ' ' + courseCompareId + "\\" + "students" + "\\" + "students " + newYear + ".json"
                                            if not os.path.isfile(studentsComparePath):
                                                continue
                                            with open(studentsComparePath, encoding="utf8") as studentsCompareFile:
                                                studentsCompareList = json.load(studentsCompareFile)
                                            checkedCourses += 1
                                            courseEnded = False                                            
                                            for currentStudent in studentsCompareList["students"]:
                                                currentStudentUsername = currentStudent["username"]
                                                currentStudentDegree = student["degree"]["acronym"][1:]
                                                if studentId == currentStudentUsername and getDegreePairs(currentStudentDegree, studentDegree):
                                                    nonlocal reproval
                                                    reproval += 1
                                                    return                        
                        if os.path.isfile(degreePath + "\\" + splittedDegreeName.lower() + " " + nextYear + ".json"):
                            with open(path + nextYear + ".json", encoding="utf8") as nextDegreesFile:
                                nextDegreesList = json.load(nextDegreesFile)                         
                            if studentChangedCourse(studentId, nextDegreesList, key, degreeTypeParsed, splittedDegreeName, courseFullName):
                                reproval +=1
                                return
                    doLoop()
                if int(studentsNumber) == 0 or (courseEnded and checkedCourses == 0) or int(currentYear) == 2017:
                    approvalPercentage = "null"
                else:
                    approvalPercentage = str(100 - reproval / int(studentsNumber) * 100) + '%'
                file = open(degreePath + "\\" + courseName + " " + courseId + "\\" + "quc" + "\\" + "approval " + newKey + ".txt","w")
                file.write(str(approvalPercentage))

def studentChangedCourse(studentId, degreesList, year, currentDegreeType, currentDegree, currentCourse):
    path = os.getcwd() + "\\json\\degrees"
    for degree in range(0, len(degreesList)):
        degreeName = degreesList[degree]["name"]
        degreeType = degreesList[degree]["type"]
        degreeAcronym = degreesList[degree]["acronym"]
        degreeTypeParsed = degreeType.split(' Bolonha',1)[0]
        if 'Diploma' in degreeTypeParsed or getDegreePairs(currentDegree, degreeName) == True:
            continue
        if ('Licenciatura' in currentDegreeType and 'Mestrado' not in degreeTypeParsed) or ('Mestrado' in currentDegreeType and 'Licenciatura' not in degreeTypeParsed):
            degreePath = path + "\\" + degreeAcronym
            firstYear = int(year.split('/',1)[0]) + 1
            secondYear = int(year.split('/',1)[1]) + 1
            parsedYear = str(firstYear) + ' ' + str(secondYear)
            coursesListPath = degreePath + "\\" + degreeName.lower() + " " + parsedYear + ".json" 
            if not os.path.isfile(coursesListPath):
                continue
            coursesFile = open(coursesListPath, "r", encoding="utf-8")
            courseList = json.load(coursesFile)
            for course in range(0, len(courseList)):
                courseName = courseList[course]["acronym"]
                courseFullName = courseList[course]["name"]
                courseId = courseList[course]["id"]
                studentsPath = degreePath + "\\" + courseName + " " + courseId + "\\" + "students" + "\\" + "students " + parsedYear + ".json"
                if not os.path.isfile(studentsPath):
                    continue            
                studentsFile = open(studentsPath, "r")
                studentsList = json.load(studentsFile)
                if getCoursePairs(courseFullName, currentCourse):
                    for currentStudent in studentsList["students"]:
                        currentStudentUsername = currentStudent["username"]
                        currentStudentDegree = currentStudent["degree"]["acronym"]
                        currentStudentDegree = currentStudentDegree[1:]
                        parsedCurrentDegree = degreeAcronym[1:]
                        if studentId == currentStudentUsername and getDegreePairs(currentStudentDegree, parsedCurrentDegree):
                            return True
    return False        

def getCoursePairs(course, course1):
    if course == course1:
        return True
    for courseGroup in coursePairs:
        if course in courseGroup and course1 in courseGroup:
            return True
    return False            
    
def getDegreePairs(degree, degree1):
    if degree == degree1:
        return True
    if degree in degreePairs:
        if degreePairs.get(degree) == degree1:
            return True
    if degree1 in degreePairs:
        if degreePairs[degree1] == degree:        
            return True
    else:
        return False
    
def retrieveAcronym(courseName, acronymList):
    for key, value in acronymList.items():
        if value == courseName:
            return key
    return ''
    
def compareAcronym(courseName, acronymList):
    parsedCourseName = unicodedata.normalize('NFKD', courseName).encode('ASCII','ignore').decode('utf-8').split(' (',1)[0].split('(',1)[0].lower()
    acronym = retrieveAcronym(parsedCourseName, acronymList)
    if acronym != '':
        return acronym
    for courseGroup in coursePairs:
        if courseName in courseGroup:
            for course in courseGroup:               
                parsedCourse = unicodedata.normalize('NFKD', course).encode('ASCII','ignore').decode('utf-8').split(' (',1)[0].split('(',1)[0].lower()            
                acronym = retrieveAcronym(parsedCourse, acronymList)
                if acronym != '':
                    return acronym
    return ''

def connectDB():
    filterwarnings('ignore', category = pymysql.Warning)    
    connection = pymysql.connect(host='localhost', port=3306, user='root', passwd='', autocommit=True)
    cursor = connection.cursor()  
    cursor.execute('CREATE DATABASE IF NOT EXISTS tecnicoviz1')  
    connection.select_db('tecnicoviz1')  
    return connection, cursor
                        
def populateDB():
    connection, cursor = connectDB()
    cursor.execute("DROP TABLE IF EXISTS Courses")
    cursor.execute("DROP TABLE IF EXISTS Degrees")
    cursor.execute("DROP TABLE IF EXISTS Students")
    cursor.execute("DROP TABLE IF EXISTS Teachers")
    cursor.execute("CREATE TABLE IF NOT EXISTS Degrees (ID BIGINT NOT NULL, degreeAcronym VARCHAR(20) NOT NULL, degreeName VARCHAR(80) NOT NULL, degreeType VARCHAR(50) NOT NULL, studentsNumberAverage INT, year INT NOT NULL, term INT NOT NULL, PRIMARY KEY (ID, year, term))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Courses (ID BIGINT NOT NULL, courseName VARCHAR(100) NOT NULL, courseAcronym VARCHAR(30) NOT NULL, degreeId BIGINT NOT NULL, degreeType VARCHAR(50) NOT NULL, degreeAcronym VARCHAR(20) NOT NULL, degreeName VARCHAR(80) NOT NULL, studentsNumber INT, year INT NOT NULL, term INT NOT NULL, credits DOUBLE, evaluationType VARCHAR(10) NOT NULL, PRIMARY KEY (ID, degreeAcronym), FOREIGN KEY (degreeId) REFERENCES Degrees(ID))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Students (username VARCHAR(20) NOT NULL, degreeAcronym VARCHAR(20) NOT NULL, courseId BIGINT NOT NULL, courseAcronym VARCHAR(50) NOT NULL, year INT NOT NULL, term INT NOT NULL, PRIMARY KEY (username, courseAcronym, year, term), FOREIGN KEY (courseId) REFERENCES Courses(ID))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Teachers (username VARCHAR(20) NOT NULL,  name VARCHAR(100) NOT NULL, degreeAcronym VARCHAR(20) NOT NULL, courseId BIGINT NOT NULL, courseAcronym VARCHAR(50) NOT NULL, year INT NOT NULL, term INT NOT NULL, teacherScore DOUBLE, PRIMARY KEY (username, degreeAcronym, courseAcronym, year, term), FOREIGN KEY (courseId) REFERENCES Courses(ID))")
    path = os.getcwd() + "\\json\\degrees"  
    # Load academic terms json file
    termsFile = open(os.getcwd() + "\\json\\academicTerms.json", "r")
    termsList = json.load(termsFile)
    termsList = sorted(termsList, key=termsList.__getitem__, reverse = True)
    repeatedAcronym = {}
    formattedAcronym = ''
    stopWords = ["de", "do", "e", "o", "da", "a", "em", "com", "por", "das", "dos", 'para']
    for key in termsList:
        newKey, year = getYear(key)
        if not os.path.isfile(path + newKey + ".json") or int(year) < 2001:
            continue
        degreesFile = open(path + newKey + ".json", "r", encoding="utf-8")
        degreesList = json.load(degreesFile)         
        degreesList = sorted(degreesList, key=lambda k: k['acronym'])
        for i in range(0, len(degreesList)):             
            degreeName, degreeId, degreeTypeParsed, degreeAcronym, degreePath = getDegree(degreesList[i], path)
            if degreeAcronym == 'LEIC-Taguspark-pB':
                degreeAcronym = 'LEIC-T-pB'
            coursesListPath = degreePath + "\\" + degreeName.lower() + " " + newKey + ".json"
            if not os.path.isfile(coursesListPath) or 'Diploma' in degreeTypeParsed or degreeAcronym == 'LEECT-pB':
                continue       
            coursesFile = open(coursesListPath, "r", encoding="utf-8")
            courseList = json.load(coursesFile)  
            for j in range(0, len(courseList)):
                courseName, courseFullName, courseTerm, courseId, coursePath, courseCredits = getCourse(courseList[j], degreePath, key)  
                courseInfo = coursePath + "\\" + courseName.lower() + " " + newKey + ".json"
                if not os.path.isfile(courseInfo):
                    continue
                studentsPath = degreePath + "\\" + courseName + " " + courseId + "\\" + "students" + "\\" + "students " + newKey + ".json"
                if not os.path.isfile(studentsPath):
                    continue 
                studentsFile = open(studentsPath, "r")
                studentsList = json.load(studentsFile)
                studentsNumber = 0
                parsedDegreeAcronym = degreeAcronym[1:]
                for student in studentsList["students"]:
                    studentId = student["username"]
                    studentDegree = student["degree"]["acronym"]
                    studentDegree = studentDegree[1:]  
                    if getDegreePairs(parsedDegreeAcronym, studentDegree):
                        studentsNumber += 1                    
                    else:
                        continue                
                courseInfoFile = open(courseInfo, "r", encoding="utf-8")
                courseInfoList = json.load(courseInfoFile) 
                evaluation = courseInfoList["evaluationMethod"]                
                try:
                    if courseInfoList["competences"] == []:
                        raise IndexError                    
                    for degrees in courseInfoList["competences"]:
                        for eachDegree in degrees:
                            if eachDegree == 'degrees':
                                fileDegreeName = degrees[eachDegree][0]["name"]
                                fileDegreeName = fileDegreeName.replace(' Bolonha','')
                                for info in range(0, len(degrees[eachDegree])):
                                    fileDegreeName = degrees[eachDegree][info]["name"]
                                    fileDegreeName = fileDegreeName.replace(' Bolonha','') 
                                    if fileDegreeName.split("em ", 1)[1] == degreeName:
                                        formattedAcronym = degrees[eachDegree][info]["acronym"][0:7].upper()
                                    else:
                                        continue
                            else:
                                continue
                except IndexError:
                    formattedAcronym = ''
                    formattedAcronym = ''.join(i for i in courseName if not i.isdigit() and i != '.')
                    formattedAcronym = formattedAcronym.replace('-', '').replace('�', '').replace(' ', '').split("_",1)[0][0:7].upper()
                evaluationPath = coursePath + "\\" + "evaluations" + "\\" + "evaluation " + newKey + ".json"                
                if not os.path.isfile(evaluationPath):
                    continue                
                evaluationFile = open(evaluationPath, "r", encoding="utf8")
                evaluationList = json.load(evaluationFile)
                evaluationType = "Project"
                for k in range(0, len(evaluationList)):
                    try:
                        evMethod = evaluationList[k]["type"]
                        if evMethod == 'FINAL_EVALUATION':
                            raise KeyError
                    except KeyError:
                        evMethod = evaluation
                        if evMethod is None:
                            evaluationUrl = courseInfoList["url"] + '/avaliacao'
                            evaluationUrl = unicodedata.normalize('NFKD', evaluationUrl).encode('ASCII','ignore').decode('utf-8')
                            try:
                                with urllib.request.urlopen(evaluationUrl) as response:
                                    evMethod = response.read().decode('utf-8')                  
                                    evMethod = evMethod.replace("Testes/Exames", '').replace("Exame: �poca Especial", '')
                            except urllib.error.HTTPError:
                                    evaluationType = "null"
                                    evMethod = "null"
                    if evMethod == "TEST" or 'testes' in evMethod.lower():
                        evaluationType = "Test"
                        break
                    if evMethod == "EXAM" or 'exame' in evMethod.lower():
                        evaluationType = "Exam"
                infoToExtract = False
                teacherInfo = {}
                teacherData = {}
                teacherName = ''
                qucPath = coursePath + "\\" + "quc" + "\\" + "quc " + newKey + ".txt"
                if os.path.isfile(qucPath):                      
                    with open(qucPath, encoding="utf8") as file:
                        skip = True
                        for line in file:
                            line = line.replace('\n','')
                            if "Avalia��o dos QUC" in line:
                                skip = False
                            if infoToExtract:
                                if "respostas insuficiente" not in line and not skip:
                                    teacherInfo.setdefault(teacherName, []).append(float(line))
                                else:
                                    line = "NULL"
                                    teacherInfo.setdefault(teacherName, []).append(line)
                                infoToExtract = False
                            if 'Avalia��o do professor' in str(line):
                                teacherName = line.split('Avalia��o do professor ',1)[1]
                                infoToExtract = True  
                                for teacher in courseInfoList["teachers"]:
                                    if teacherName == teacher["name"]:
                                        teacherData[teacherName] = teacher["istId"] 
                if '(ead)' not in courseFullName.lower() and '2� Fase' not in courseFullName.lower():
                    parsedCourseName = unicodedata.normalize('NFKD', courseFullName).encode('ASCII','ignore').decode('utf-8').split(' (',1)[0].split('(',1)[0].lower()
                acronym = compareAcronym(courseFullName, repeatedAcronym)
                if acronym != '':
                    formattedAcronym = acronym
                else:
                    if formattedAcronym in repeatedAcronym and getCoursePairs(repeatedAcronym[formattedAcronym], parsedCourseName) == False or formattedAcronym == '' or formattedAcronym == '$':
                        courseNameStop = ' '.join(filter(lambda word: word not in stopWords, parsedCourseName.split())).title()
                        formattedAcronym = re.sub('[^A-Z]', '', courseNameStop)
                        formattedAcronym = formattedAcronym.replace('-', '').replace('_', '').replace('�', '').replace(' ', '')[0:7]
                        if formattedAcronym in repeatedAcronym:
                            formattedAcronym = "".join(word[0:2] for word in courseNameStop.split())[0:7].upper()
                        if formattedAcronym in repeatedAcronym:
                            formattedAcronym = "".join(word[0:3] for word in courseNameStop.split())[0:7].upper()   
                        if formattedAcronym in repeatedAcronym:
                            formattedAcronym = "".join(word[0:4] for word in courseNameStop.split())[0:7].upper()
                        if formattedAcronym in repeatedAcronym:
                            formattedAcronym = "".join(word[0:1]+word[5:6]+word[8:9] for word in courseNameStop.split())[0:7].upper()
                query = "INSERT INTO courses (ID, courseName, courseAcronym, degreeId, degreeType, degreeAcronym, degreeName, studentsNumber, year, term, credits, evaluationType) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                queryTeachers = "INSERT INTO teachers (username, name, degreeAcronym, courseId, courseAcronym, year, term, teacherScore) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                try:
                    cursor.execute(query, (int(courseId), courseFullName, formattedAcronym, degreeId, degreeTypeParsed, degreeAcronym, degreeName, studentsNumber, year, int(courseTerm), float(courseCredits), evaluationType)) 
                except pymysql.err.IntegrityError:
                    pass
                try:
                    if teacherInfo != {}:
                        for teacher in teacherInfo:
                            teacherUsername = teacherData[teacher]
                            totalScore = 0
                            for score in teacherInfo[teacher]:
                                if score == "NULL":
                                    totalScore = None
                                else:
                                    totalScore += score
                                cursor.execute(queryTeachers, (teacherUsername, teacher, degreeAcronym, int(courseId), formattedAcronym, year, int(courseTerm), totalScore))
                    else:
                        for teacher in courseInfoList["teachers"]:
                            teacherUsername = teacher["istId"]
                            teacherName = teacher["name"]
                            queryTeachers = "INSERT INTO teachers (username, name, degreeAcronym, courseId, courseAcronym, year, term, teacherScore) VALUES (%s, %s, %s, %s, %s, %s, %s, NULL)"
                            cursor.execute(queryTeachers, (teacherUsername, teacherName, degreeAcronym, int(courseId), formattedAcronym, year, int(courseTerm)))
                except:
                    pass
                populateStudents(cursor, int(courseId), formattedAcronym, degreeAcronym, coursePath, newKey, courseTerm)
                if formattedAcronym not in repeatedAcronym:
                    repeatedAcronym[formattedAcronym] = parsedCourseName
                query = "INSERT INTO degrees (ID, degreeAcronym, degreeName, degreeType, year, term) VALUES (%s, %s, %s, %s, %s, %s)"
                try:
                    cursor.execute(query, (int(degreeId), degreeAcronym, degreeName, degreeTypeParsed, year, int(courseTerm)))
                except pymysql.err.IntegrityError:
                    pass            
    connection.close()

def populateStudents(cursor, courseId, courseName, degreeName, coursePath, year, term): 
    studentsPath = coursePath + "\\" + "students" + "\\" + "students " + year + ".json"
    parsedYear = year.split(' ',1)[0]
    parsedDegree = degreeName[1:]
    if not os.path.isfile(studentsPath):
        return                
    studentsFile = open(studentsPath, "r")
    studentsList = json.load(studentsFile)
    for currentStudent in studentsList["students"]:
        studentUsername = currentStudent["username"]
        studentDegree = currentStudent["degree"]["acronym"]
        parsedStudentDegree = studentDegree[1:]
        if studentDegree == "":
            studentDegree = "ISOL"
        if parsedStudentDegree == parsedDegree:
            query = "INSERT INTO students (username, degreeAcronym, courseId, courseAcronym, year, term) VALUES (%s, %s, %s, %s, %s, %s)"
            try:
                cursor.execute(query, (studentUsername, degreeName, courseId, courseName, parsedYear, term))   
            except pymysql.err.IntegrityError:
                pass

def coursesQucEvaluation():
    connection, cursor = connectDB()
    try:
        cursor.execute('ALTER TABLE courses ADD grades DOUBLE')
    except pymysql.err.InternalError:
        pass   
    try:
        cursor.execute('ALTER TABLE courses ADD approval DOUBLE(5,2)')
    except pymysql.err.InternalError:
        pass    
    try:
        cursor.execute('ALTER TABLE courses ADD quc DOUBLE')
    except pymysql.err.InternalError:
        pass    
    path = os.getcwd() + "\\json\\degrees"
    # Load academic terms json file
    termsFile = open(os.getcwd() + "\\json\\academicTerms.json", "r")
    termsList = json.load(termsFile) 
    for key in termsList:
        newKey, year = getYear(key)
        if not os.path.isfile(path + newKey + ".json") or int(year) < 2001:
            continue
        degreesFile = open(path + newKey + ".json", "r", encoding="utf-8")
        degreesList = json.load(degreesFile)         
        degreesList = sorted(degreesList, key=lambda k: k['acronym'])
        for i in range(0, len(degreesList)):             
            degreeName, degreeId, degreeTypeParsed, degreeAcronym, degreePath = getDegree(degreesList[i], path)
            if degreeAcronym == 'LEIC-Taguspark-pB':
                degreeAcronym = 'LEIC-T-pB'            
            coursesListPath = degreePath + "\\" + degreeName.lower() + " " + newKey + ".json"
            if not os.path.isfile(coursesListPath) or 'Diploma' in degreeTypeParsed or degreeAcronym == 'LEECT-pB':
                continue       
            coursesFile = open(coursesListPath, "r", encoding="utf-8")
            courseList = json.load(coursesFile)  
            for j in range(0, len(courseList)):
                courseName, courseFullName, courseTerm, courseId, coursePath, courseCredits = getCourse(courseList[j], degreePath, key)
                qucPath = coursePath + "\\" + "quc" + "\\" + "quc " + newKey + ".txt"
                approval = ""
                grade = ""
                if os.path.isfile(qucPath) and 'Disserta��o' not in courseFullName:        
                    with open(qucPath, encoding="utf8") as file:
                        for line in file:
                            if '%' in line:
                                approval = line.split('%',1)[0]
                                break                      
                if approval == "":
                    approvalPath = coursePath + "\\" + "quc" + "\\" + "approval " + newKey + ".txt"                
                    if os.path.isfile(approvalPath):
                        with open(approvalPath, encoding="utf8") as file:
                            for line in file:
                                if '%' in line:
                                    approval = line.split('%',1)[0]
                                    break
                qucScore = 0
                numberOfScores = 0
                infoToExtract = False
                if os.path.isfile(qucPath):
                    with open(qucPath, encoding="utf8") as file:
                        for line in file:
                            line = line.replace('\n','')
                            if 'do professor' in str(line):
                                break                        
                            if infoToExtract:
                                if line == '-':
                                    continue
                                qucScore += float(line)
                                numberOfScores += 1
                            if 'Avalia��o dos QUC' == line:
                                infoToExtract = True
                    infoToExtract = False
                    with open(qucPath, encoding="utf8") as file:
                        for line in file:
                            line = line.replace('\n','')                      
                            if infoToExtract:
                                grade = line
                                break
                            if 'M�dia' in line:
                                infoToExtract = True
                if approval == "null" or approval == "":
                    approval = None
                queryUpdate = "UPDATE courses SET approval = %s WHERE ID = %s and degreeAcronym = %s"
                cursor.execute(queryUpdate, (approval, courseId, degreeAcronym))  
                if numberOfScores != 0:
                    qucScore /= numberOfScores
                else:
                    qucScore = None
                queryUpdate = "UPDATE courses SET quc = %s WHERE ID = %s and degreeAcronym = %s"
                cursor.execute(queryUpdate, (qucScore, int(courseId), degreeAcronym))
                if "" == grade:
                    grade = None
                queryUpdateGrade = "UPDATE courses SET grades = %s WHERE ID = %s and degreeAcronym = %s"
                cursor.execute(queryUpdateGrade, (grade, courseId, degreeAcronym))
def terms():
    connection, cursor = connectDB()
    cursor.execute("DROP TABLE IF EXISTS Terms")
    cursor.execute("CREATE TABLE IF NOT EXISTS Terms (year INT NOT NULL, term INT NOT NULL, PRIMARY KEY (year, term))")    
    cursor.execute("SELECT year,term from Courses group by year,term")
    row = cursor.fetchall() 
    terms = cursor.rowcount
    for i in range(0, terms):   
        year = str(row[i][0])
        term = str(row[i][1])
        print(year, term)
        insertQuery = "INSERT INTO Terms (year, term) VALUES (%s, %s)"
        cursor.execute(insertQuery, (year, term))

def getDegree(degrees, path):        
    degreeName = degrees["name"]
    degreeId = degrees["id"]
    degreeType = degrees["type"]
    degreeAcronym = degrees["acronym"]
    degreeTypeParsed = degreeType.split(' Bolonha',1)[0]
    degree = degreeTypeParsed + ' em ' + degreeName
    degreePath = path + "\\" + degreeAcronym        
    return degreeName, degreeId, degreeTypeParsed, degreeAcronym, degreePath

def getYear(key):
    newKey = key.replace("/", " ")
    year = key.split('/',1)[0]
    return newKey, year
             
def getCourse(courses, degreePath, key):
    courseName = courses["acronym"]
    courseFullName = courses["name"]
    courseFullName = courseFullName.replace("�", "-")
    courseCredits = courses["credits"]
    courseTerm = courses["academicTerm"]
    courseTerm = courseTerm.replace('Semestre ' + key, '').replace('�', '')
    courseId = courses["id"]
    coursePath = degreePath + "\\" + courseName + " " + courseId
    return courseName, courseFullName, courseTerm, courseId, coursePath, courseCredits
    
def degreeApprovalsAverage():
    connection, cursor = connectDB()
    try:
        cursor.execute('ALTER TABLE Degrees ADD approvalAverage DOUBLE(5,2)')
    except pymysql.err.InternalError:
        pass    
    cursor.execute("SELECT degreeAcronym, year, term from courses group by degreeAcronym, year, term")
    row = cursor.fetchall() 
    numRowsDegrees = cursor.rowcount
    for i in range(0, numRowsDegrees):   
        degree = str(row[i][0])
        year = str(row[i][1])
        term = str(row[i][2])
        queryApproval = "SELECT AVG(approval) FROM courses WHERE term = %s and year = %s and degreeAcronym = %s"
        cursor.execute(queryApproval, (term, year, degree))
        result = cursor.fetchall()
        numRowsAverage = cursor.rowcount
        for j in range(0, numRowsAverage):
            approvalAverage = result[j][0]
            queryUpdate = "UPDATE Degrees SET approvalAverage = %s WHERE degreeAcronym = %s and year = %s and term = %s"
            cursor.execute(queryUpdate, (approvalAverage, degree, int(year), int(term)))

def degreeGradesAverage():
    connection, cursor = connectDB()
    try:
        cursor.execute('ALTER TABLE Degrees ADD gradesAverage DOUBLE(5,2)')
    except pymysql.err.InternalError:
        pass    
    cursor.execute("SELECT degreeAcronym, year, term from courses group by degreeAcronym, year, term")
    row = cursor.fetchall() 
    numRowsDegrees = cursor.rowcount
    for i in range(0, numRowsDegrees):   
        degree = str(row[i][0])
        year = str(row[i][1])
        term = str(row[i][2])
        queryApproval = "SELECT AVG(grades) FROM courses WHERE term = %s and year = %s and degreeAcronym = %s"
        cursor.execute(queryApproval, (term, year, degree))
        result = cursor.fetchall()
        numRowsAverage = cursor.rowcount
        for j in range(0, numRowsAverage):
            gradesAverage = result[j][0]
            queryUpdate = "UPDATE Degrees SET gradesAverage = %s WHERE degreeAcronym = %s and year = %s and term = %s"
            cursor.execute(queryUpdate, (gradesAverage, degree, int(year), int(term)))

def degreeQucAverage():
    connection, cursor = connectDB()
    try:
        cursor.execute('ALTER TABLE Degrees ADD qucAverage DOUBLE(5,2)')
    except pymysql.err.InternalError:
        pass    
    cursor.execute("SELECT degreeAcronym, year, term from courses group by degreeAcronym, year, term")
    row = cursor.fetchall() 
    numRowsDegrees = cursor.rowcount
    for i in range(0, numRowsDegrees):   
        degree = str(row[i][0])
        year = str(row[i][1])
        term = str(row[i][2])
        queryQuc = "SELECT AVG(quc) FROM courses WHERE term = %s and year = %s and degreeAcronym = %s"
        cursor.execute(queryQuc, (term, year, degree))
        result = cursor.fetchall()
        numRowsAverage = cursor.rowcount
        for j in range(0, numRowsAverage):
            qucAverage = result[j][0]
            queryUpdate = "UPDATE Degrees SET qucAverage = %s WHERE degreeAcronym = %s and year = %s and term = %s"
            cursor.execute(queryUpdate, (qucAverage, degree, int(year), int(term)))
            
def degreeStudentsAverage():
    connection, cursor = connectDB()    
    cursor.execute("SELECT degreeAcronym, year, term from courses group by degreeAcronym, year, term")
    row = cursor.fetchall() 
    numRowsDegrees = cursor.rowcount
    for i in range(0, numRowsDegrees):   
        degree = str(row[i][0])
        year = str(row[i][1])
        term = str(row[i][2])
        queryStudents = "SELECT SUM(studentsNumber) FROM courses WHERE term = %s and year = %s and degreeAcronym = %s"
        cursor.execute(queryStudents, (term, year, degree))
        result = cursor.fetchall()
        numRowsAverage = cursor.rowcount
        for j in range(0, numRowsAverage):
            studentsAverage = result[j][0]
            queryUpdate = "UPDATE Degrees SET studentsNumberAverage = %s WHERE degreeAcronym = %s and year = %s and term = %s"
            cursor.execute(queryUpdate, (studentsAverage, degree, int(year), int(term)))

def courseApprovalsAverage():
    connection, cursor = connectDB()
    try:
        cursor.execute('ALTER TABLE Courses ADD approvalAverage DOUBLE(5,2)')
    except pymysql.err.InternalError:
        pass    
    cursor.execute("SELECT courseAcronym, year, term from courses group by courseAcronym, year, term")
    row = cursor.fetchall() 
    numRowsDegrees = cursor.rowcount
    for i in range(0, numRowsDegrees):   
        degree = str(row[i][0])
        year = str(row[i][1])
        term = str(row[i][2])
        queryApproval = "SELECT AVG(approval) FROM courses WHERE term = %s and year = %s and courseAcronym = %s"
        cursor.execute(queryApproval, (term, year, degree))
        result = cursor.fetchall()
        numRowsAverage = cursor.rowcount
        for j in range(0, numRowsAverage):
            approvalAverage = result[j][0]
            queryUpdate = "UPDATE Courses SET approvalAverage = %s WHERE courseAcronym = %s and year = %s and term = %s"
            cursor.execute(queryUpdate, (approvalAverage, degree, int(year), int(term))) 

#Retrieve data       
fenixEduDataRetrieval()
#Calculate approvals
approvalsCalculation()

# Database Functions
populateDB()
studentsReprovals()
coursesQucEvaluation() 
terms()
degreeApprovalsAverage()
courseApprovalsAverage()
degreeQucAverage()
degreeGradesAverage()
degreeStudentsAverage()
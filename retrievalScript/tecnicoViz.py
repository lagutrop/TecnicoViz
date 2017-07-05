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
                ["Comunicação de Áudio e Vídeo", "Comunicação Multimédia"],
                ["Modelização de Sistemas Energéticos", "Modelização e Economia de Sistemas Energéticos"],
                ["Pgp - Business Intelligence", "Pgp - Business Intelligence and Activity Monitoring"],
                ["Pgp - Estratégia e Sistemas de Informação", "Estratégia, Governação e Transformação Organizacional"],
                ["Pgp - Modelação em Engenharia Empresarial", "Pgp - Engenharia Empresarial I"],
                ["Pgp - Teoria dos Sistemas e Modelação Conceptual", "Pgp - Engenharia Empresarial II"],
                ["Pgp - Engenharia Empresarial e Integração de Sistemas de Informação", "Pgp - Engenharia Empresarial III"],
                ["Pgp - Gestão de Projectos Informáticos", "Pgp - Gestão de Projectos e Programas"],
                ["Pgp - Eengenharia Empresarial III", "Pgp - Engenharia Empresarial III"],
                ["Eco-Hidráulica e Modelação em Sistemas Fluviais", "Ecohidráulica e Modelação em Sistemas Fluviais"],
                ["Tópicos Avançados em Fusão Nuclear", "Tópicos Avançados em Física dos Plasmas, Fusão Nuclear e Lasers"],
                ["Estrutura e Comportamento dos Materiais de Construção", "Curso Avançado em Estrutura e Comportamento dos Materiais de Construção"],
                ["Métodos de Simulação do Comportamento Térmico e Acústico de Edifícios", "Curso Avançado em Comportamento Térmico e Acústico de Edifícios"],
                ["Reabilitação de Edifícios e Estruturas Especiais: Estudos Avançados", "Curso Avançado em Reabilitação de Edifícios e Estruturas Especiais"],
                ["Estabilidade e Estruturas Metálicas ? Curso Avançado", "Curso Avançado em Estabilidade e Estruturas Metálicas"],
                ["Dinâmica de Estruturas - Curso Avançado", "Curso Avançado em Dinâmica de Estruturas"],
                ["Modelação de Estruturas - Curso Avançado", "Curso Avançado em Modelação de Estruturas"],
                ["Mecânica Estatística e Transições de Fase.", "Mecânica Estatística e Transições de Fase"],
                ["Teoria do Campo Avançada", "Teoria do Campo"],
                ["Métodos Computacionais", "Métodos Computacionais e Optimização"],
                ["Sistemas de Comunicação Via Satélite", "Sistemas de Comunicação por Satélite"],
                ["Qualidade de Serviço em Redes de Dados", "Qualidade de Serviço em Redes de Dados por Pacotes"],
                ["Tópicos Avançados em Arquitectura e Sistemas Distribuídos", "Tópicos Avançados em Arquitecturas e Sistemas Distribuídos"],
                ["Engenharia de Ontologias e Semântica de Redes", "Engenharia de Ontologias e Web Semântica"],
                ["Seminário de Investigação em Matemática - Semestre 2", "Seminário de Investigação em Matemática"],
                ["Química de Interfaces/Superfícies, Interfaces e Colóides", "Superfícies, Interfaces e Colóides"],
                ["Análise Numérica Funcional e Optimização", "Análise Funcional Aplicada / Análise Numérica Funcional e Optimização"],
                ["Modelos Matemáticos em Hemodinâmica", "Métodos Matemáticos em Hemodinâmica"],
                ["Modelação e Análise de Sistemas de Telecomunicações por Fibra Óptica", "Sistemas Modernos de Telecomunicações por Fibra Óptica"],
                ["Planeamento de Sistemas de Energia", "Gestão e Planeamento de Sistemas de Energia"],
                ["Optimização - Programação Não Linear", "Optimização Não Linear", "Optimização", "Optimização Nãolinear ", "Optimização Nãolinear"],
                ["Robótica Avançada", "Tópicos Avançados em Robótica"],
                ["Projecto de Circuitos Integrados para Rádio Frequência", "Circuitos Integrados para Rádio Frequência"],
                ["Sistemas Dinâmicos de Eventos Discretos", "Sistemas de Eventos Discretos"],
                ["Projecto de Geradores Eléctricos de Baixa Velocidade para Aproveitamentos de Energias", "Projecto de Geradores Eléctricos de Baixa Velocidade para Aproveitamentos de Energias Renováveis"],
                ["Processamento de Imagem e Vídeo", "Processamento de Imagem e Video (Cmu)"],
                ["Instrumentação e Aquisição de Sinais", "Instrumentação e Aquisição de Sinais em Bioengenharia"],
                ["Complementos de Análise Complexa", "Análise Complexa"],
                ["Análise Numérica Funcional e Optimização", "Análise Funcional Aplicada", "Análise Funcional Aplicada / Análise Numérica Funcional e Optimização", "Análise Funcional Aplicada"],
                ["Electrónica e Instrumentação", "Sinais e Sistemas Mecatrónicos"],
                ["Materiais e Processos de Construção", "Prospecção Geofisica e Sondagens"],
                ["O Papel do Engenheiro", "Seminários de Engenharia de Materiais II"],
                ["Design e Materiais", "Design e Selecção de Materiais"],
                ["Expressão Oral e Escrita-Materiais", "Seminários de Engenharia de Materiais I"],
                ["Sistemas de Informação e Bases de Dados / Bases de Dados", "Bases de Dados", "Bases de Dados/Sistemas de Informação e Bases de Dados"],
                ["Portfolio I", "Portfolio Pessoal I"],
                ["Digital Systems", "Sistemas Digitais", "Sistemas Digitais - 2ª Fase", "Introdução à Arquitetura de Computadores"],
                ["Arquitectura de Computadores", "Arquitecturas de Computadores", "Organização de Computadores"],
                ["Modelação", "Análise e Modelação de Sistemas"],
                ["Cálculo Diferencial e Integral I - 2ª Fase", "Cálculo Diferencial e Integral I", "Cálculo Diferencial e Integral I - 2ª Fase - Alameda"],
                ["Teoria da Computação - 2ª Fase", "Teoria da Computação"],
                ["Álgebra Linear", "Álgebra Linear - 2ª Fase", " Álgebra Linear - 2ª Fase - Alameda", "Álgebra Linear A"], 
                ["Fundamentos da Programação / Elementos de Programação - 2ª Fase", "Fundamentos da Programação", "Elementos de Programação/Fundamentos de Programação/Programação", "Elementos de Programação/Fundamentos de Programação/Programação - 2ª Fase", "Fundamentos da Programação/Programação", "Programação", "Elementos de Programação", "Fundamentos de Programação/Programação", "Fundamentos da Programação / Elementos de Programação", "Fundamentos da Programação - 2ª Fase", 'Fundamentos de Programação'],
                ["Introdução aos Algoritmos e Estruturas de Dados / Algoritmos e Estrutura de Dados", "Introdução aos Algoritmos e Estruturas de Dados/Algoritmos e Estrutura de Dados", "Introdução aos Algoritmos e Estruturas de Dados", "Introdução aos Algoritmos e Estrutura de Dados", "Algoritmos e Estrutura de Dados"],
                ["Introdução à Interface Pessoa-Máquina", "Introdução às Interfaces Pessoa-Máquina"],
                ["Teoria dos Circuitos e Fundamentos de Electrónica", "Teoria dos Circuitos e Fund. de Electrónica", "Introdução aos Circuitos e Sistemas Electrónicos"],
                ["Introdução à Electrónica das Comunicações", "Electrónica dos Sistemas Embebidos"],
                ["Redes Integradas de Comunicações", "Arquitecturas de Redes"],
                ["Sinais e Sistemas", "Sistemas e Sinais"],
                ["Portfolio Pessoal II", "Portfolio II", "Comunicação Oral e Escrita"],
                ["Gestão de Redes e Serviços", "Gestão de Redes e Serviços/Gestão e Segurança de Redes", "Gestão e Segurança de Redes / Gestão de Redes e Serviços", "Gestão e Segurança de Redes"],
                ["Controlo", "Fundamentos de Controlo"],
                ["Instrumentação e Medidas", "Instrumentação e Aquisição de Sinais", "Instrumentação Electrónica/Instrumentação e Medidas"],
                ["Electrotecnia e Máquinas Eléctricas", "Sistemas Eléctricos e Electromecânicos", "Sistemas Electromecânicos"],
                ["Programação de Sistemas", "Programação de Sistemas Computacionais"],
                ["Processos de Fabrico", "Electrónica dos Sistemas Embebidos"],
                ["Direito", "Direito Empresarial"],
                ["Administração e Optimização de Bases de Dados", "Administração de Dados e Sistemas de Informação"],
                ["Arquitectura Organizacional de Sistemas de Informação", "Fundamentos de Sistemas de Informação"],
                ["Tecnologia de Jogos e Simulação", "Metodologia de Desenvolvimento de Jogos"],
                ["Arquitectura, Processos e Ferramentas de Sistemas de Informação", "Arquitetura Empresarial"],
                ["Gestão e Administração de Sistemas e Redes", "Administração e Gestão de Infraestruturas de It"],
                ["Programação 3D para Simulação de Jogos", "Programação 3D"],
                ["Computação Móvel", "Computação Móvel e Ubíqua"],
                ["Gestão e Tratamento de Informação", "Análise e Integração de Dados"],
                ["Desenho e Desenvolvimento de Jogos", "Design de Jogos"],
                ["Sistemas Empresariais Integrados", "Integração Empresarial"],
                ["Plataformas para Aplicações Distribuídas na Internet", "Desenvolvimento de Aplicações Distribuídas"],
                ["Qualidade de Software", "Especificação de Software"],
                ["Portfolio III", "Portfolio Pessoal III"],
                ["Aplicações e Implementações de Algoritmos Criptográficos", "Aplicações e Implementações de Algoritmos Criptográficos / Aplica. Implementação de Sis. Segurança", "Aplicações e Implementações de Algoritmos Criptográficos / AI de Sistemas de Segurança"],
                ["Dissertação de Mestrado em Engenharia Informática e de Computadores", "Dissertação - Mestrado em Engenharia Informática e de Computadores"],
                ["Portfolio IV", "Portfolio Pessoal IV"],
                ["Plataformas para Desenvol. Aplicações de Sist. Embebidos/Aplicações para Sistemas Embebidos", "Plataformas para Desenvolvimento de Aplicações para Sistemas Embebidos", "Aplicações para Sistemas Embebidos"], 
                ["Ambientes Virtuais de Execução", "Computação em Nuvem e Virtualização"],
                ["Recuperação e Gestão de Informação", "Processamento e Recuperação de Informação"],
                ["Algoritmos e Optimização", "Algoritmos e Optimização / Optimização e Algoritmos", "Optimização e Algoritmos"],
                ["Controlo e Decisão Inteligente", "Controlo e Decisão Inteligente / Sistemas Inteligentes "],
                ["Processamento de Imagem e Visão", "Processamento de Imagem e Visão Artificial"],
                ["Sistemas Distribuídos Tolerantes a Faltas", "Sistemas de Elevada Confiabilidade"],
                ["Instrumentação e Aquisição de Sinais", "Instrumentação e Aquisição de Sinais em Bioengenharia ", "Instrumentação e Aquisição de Sinais em Bioengenharia"],
                ["Processamento Digital de Sinais", "Processamento Digital de Sinais em Bioengenharia", "Processamento de Sinais em Bioengenharia"],
                ["Engenharia de Células e Tecidos", "Engª de Células e Tecidos / Engenharia Celular"],
                ["Controlo e Operação de Sistemas de Energia", "Controlo e Optimização de Sistemas de Energia"],
                ["Sistemas Computacionais", "Sistemas Computacionais Embebidos ", "Sistemas Computacionais Embebidos"],
                ["Sistemas de Energia em Ambientes de Mercado", "Mercados de Electricidade Competitivos"],
                [" Sistemas de Informação e Bases de Dados", "Sistemas de Informação e Bases de Dados / Bases de Dados", "Sistemas de Informação e Bases de Dados"],
                ["Microprocessadores", "Microcontroladores"],
                ["Oficinas", "Laboratório de Oficinas"],
                ["Laboratório de Investigação e Desenvolvimento", "Laboratório de Inovação e Desenvolvimento"],
                ["Processos de Engenharia Química e Biológica I", "Processos de Engenharia Química e Biológica", " Processos de Engenharia Química e Biológica "],
                ["Portfolio em Engenharia Biológica", "Portfolio em Engenharia Biológica I"],
                ["Monitorização e Controlo de Bioprocessos", "Supervisão e Diagnóstico de Processos"],
                ["Planeamento Biofísico", "Planeamento Biofísico e Ordenamento do Território"],
                ["Electrodinâmica Espacial", "Ambiente Espacial"],
                ["Circuitos Eléctricos e Introdução à Electrónica", "Teoria dos Circuitos e Fundamentos de Electrónica"],
                ["Instrumentação", "Sensores e Sistemas"],
                [" Complementos de Tecnologia Mecânica", "Complementos de Tecnologia Mecânica"],
                ["Sistemas Inteligentes", "Controlo e Decisão Inteligente / Sistemas Inteligentes "],
                ["Controlo Integrado da Produção / Modelação e Controlo de Sistemas de Produção", "Controlo Integrado da Produção", "Controlo Integrado da Produção / RAAI", "Modelação e Controlo de Sistemas de Manufactura", "Modelação e Controlo de Sistemas de Manufactura / Modelação e Controlo de Sistemas de Produção", " Modelação e Controlo de Sistemas de Manufactura"],
                ["História da Cidade", "História da Cidade para Arquitectura"],
                ["Harmonização Física/Desenho", "Harmonização"],
                ["Projecto Final", "Projecto Final em Arquitectura 1 "],
                ["Dissertação/Projecto Final em Arquitectura", "Dissertação em Arquitectura"],
                ["Fundações e Obras de Aterro", "Obras de Aterro"],
                ["Dissertação de Mestrado em Engenharia Civil", "Dissertação de Mestrado em Engenharia Civil - G"],
                ["Dissertação de Mestrado em Engenharia Civil", "Dissertação de Mestrado em Engenharia Civil - C"],
                ["Dissertação de Mestrado em Engenharia Civil", "Dissertação de Mestrado em Engenharia Civil - Uts"],
                ["Dissertação de Mestrado em Engenharia Civil", "Dissertação de Mestrado em Engenharia Civil - Hrh"],
                ["Dissertação de Mestrado em Engenharia Civil", "Dissertação de Mestrado em Engenharia Civil - e"],
                ["Transporte de Mercadorias e Processos Logísticos", "Transporte de Mercadorias e Logística"],
                ["Estruturas Especiais e Fundações", "Estruturas Especiais"],
                ["Construção e Manutenção de Infra-Estruturas de Transportes", "Processos de Construção em Infraestruturas de Transportes", "Conservação de Infraestruturas de Transporte"],
                ["Gestão de Empreendimentos e de Contratos", "Empreendimentos e Contratos"],
                ["Profissionalismo e Ética", "Profissionalismo e Ética / Formação Livre III"],
                ["Gestão de Projectos I", "Gestão de Projectos", "Gestão de Projectos - Gestão de Projectos de Engenharia"],
                [" Dissertação de Mestrado em Engenharia e Gestão Industrial", "Dissertação de Mestrado em Engenharia e Gestão Industrial", "Dissertação em Engenharia e Gestão Industrial"],
                ["Análise e Gestão do Risco em Projectos", "Avaliação e Gestão do Risco em Projectos"],
                ["Formação Livre III", "Profissionalismo e Ética / Formação Livre III"],
                ["Sistemas de Processamento Digital de Sinais", "Sistemas de Processamento Digital de Sinais / Processadores de Sinal para Comunicações"],
                ["Opção de Gestão", "Opção de Gestão - 1ºSem."],
                ["Dissertação de Mestrado em Engenharia Electrónica", "Dissertação - Mestrado em Engenharia Electrónica"],
                ["Projecto em Engenharia de Redes de Comunicações", "Projecto em Engenharia de Telecomunicações e Informática"],
                ["Dissertação em Engenharia de Redes de Comunicações", "Dissertação em Engenharia de Telecomunicações e Informática"],
                ["Computação em Nuvem", "Computação em Nuvem e Virtualização"],
                ["Monitorização e Controlo", "Quimiometria, Monitorização e Controlo"],
                ["Quimiometria-Mef", "Quimiometria, Monitorização e Controlo"],
                ["Introdução às Ciências Farmacêuticas", "Ciências Farmacêuticas"],
                ["Engenharia Farmacêutica Integrada", "Engenharia Farmacêutica"],
                ["Projecto/Dissertação em Engenharia Farmacêutica", "Dissertação"],
                ["Desenvolvimento de Medicamentos: Farmacocinética e Ensaios Clínicos", "Farmacocinética no Desenvolvimento de Medicamentos"],
                ["Projecto I ? Química Terapêutica", "Projecto I - Química Terapêutica"],
                ["Introdução às Ciências de Engenharia", "Ciências de Engenharia Química"],
                ["Laboratórios de Biotecnologia I", "Laboratórios de Ciências Biológicas"],
                ["Biotecnologia e Ambiente", "Biotecnologia Ambiental"],
                ["Projecto em Engenharia e Gestão de Energia", "Projeto em Engenharia e Gestão de Energia 1"],
                ["Avaliação de Bens Imobiliários e Manutenção das Construções", "Avaliação de Bens Imobiliários"],
                ["Avaliação de Bens Imobiliários e Manutenção das Construções", "Manutenção das Construções"],
                ["Direito do Urbanismo e do Ambiente", "Direito do Urbanismo e do Ordenamento do Território"],
                ["Modelos Matemáticos em Biomedecina", "Modelos Matemáticos em Biomedicina"],
                ["Fundamentos de Lógica e Teoria da Computação(MMA)", "Fundamentos de Lógica e Teoria da Computação"],
                ["Introdução aos Processos Estocásticos(MMA)", "Introdução aos Processos Estocásticos"],
                ["Dissertação de Mestrado", "Dissertação de Mestrado em Matemática e Aplicações"],
                ["Dissertação/Projecto", "Dissertação em Engenharia de Materiais"],
                ["Dissertação/Projecto", "Projecto em Engenharia de Materiais"],
                ["Estabilização de Maciços Rochosos", "Geomecânica Aplicada à Exploração"],
                ["Dissertação/Projecto em Engª Geológica e de Minas", "Dissertação em Engenharia Geológica e de Minas"],
                ["Dissertação/Projecto em Engª Geológica e de Minas", "Projecto em Engenharia Geológica e de Minas"],
                ["Dissertação de Mestrado em Química", "Dissertação de Mestrado em Química - A"],
                ["Micro e Nanofabricação", "Técnicas de Micro e Nanofabricação"],
                ["Dissertação de Mestrado em Bioengenharia e Nanossistemas", "Dissertação de Bioengenharia e Nanossistemas", "Dissertação em Bioengenharia e Nanossistemas"],
                ["Dissertação de Mestrado em Bioengenharia e Nanossistemas", "Projecto em Bioengenharia e Nanossistemas"],
                ["Engenharia Celular", "Engª de Células e Tecidos / Engenharia Celular", "Engenharia de Células e Tecidos"],
                ["Engenharia Biomolecular", "Engenharia Biomolecular e Celular"],
                ["Laboratórios de Bioengenharia", "Laboratórios de Bioengenharia e Nanossistemas"],
                ["Química de Interfaces", "Química de Interfaces/Superfícies, Interfaces e Colóides", "Superfícies, Interfaces e Colóides"],
                ["Dissertação/Projecto - Mestrado em Engenharia e Arquitectura Naval", "Dissertação em Engenharia e Arquitectura Naval"],
                ["Gestão Urbanística", "Gestão Urbanística e Economia do Imobiliário/Gestão Urbanística"],
                ["Probabilidades e Estatística", "Introdução às Probabilidades e Estatística", "Probabilidades e Estatística/Introdução às Probabilidades e Estatística"],
                ["Dissertação em Engenharia do Ambiente", "Dissertação de Mestrado em Engenharia do Ambiente", "Dissertação/Projecto em Engenharia do Ambiente"],
                ["Desenho e Modelação Geométrica I", "Desenho e Modelação Geométrica", "Desenho e Modelação Geométrica I / Desenho e Modelação Geométrica I"],
                ["Aspectos Profissionais e Sociais da Engenharia Informática", "Computação e Sociedade"],
                ["Análise e Simulação Numérica", "Análise e Simulação Numérica / Análise Numérica II"],
                ["Ambientes e Impactes /  Ambiente Urbano e Espaço Construído", "Ambiente Urbano e Espaço Construído"],
                ["Introdução à Química-Física", "Introdução à Química-Física/Introdução à Química-Física/Química-Física de Materiais"],
                ["Probabilidades e Estatística", "Probabilidades e Estatística/Probabilidades Erros e Estatística", "Probabilidades e Estatística / Probabilidades e Estatística I"],
                ["Sistemas de Processamento Digital de Sinais /  Processadores de Sinal para Comunicações", "Processadores de Sinal para Comunicações"],
                ["Bases de Dados", "Bases de Dados/Sistemas de Informação e Bases de Dados"],
                ["Modelos Multicritério de Apoio à Decisão", "Avaliação de Projectos e Decisão Pública / Modelos Multicritério de Apoio à Decisão", "Avaliação de Projectos e Decisão Pública/Modelos Multicritério de Apoio à Decisão"],
                ["Elementos de Electrotecnia/Electrotecnia e Máquinas Eléctricas", "Elementos de Electrotecnia / Electrotecnia e Máquinas Eléctricas"],
                ["Gestão da Produção II", "Gestão da Produção e das Operações / Gestão da Produção II", "Gestão da Produção e das Operações/Gestão da Produção II", "Gestão da Produção e das Operações"],
                ["Gestão Estratégica", "Gestão Estrategica/Gestão Estratégica e Comercial"],
                ["Infraestruturas Inst.e Projectos Industriais", "Infraestruturas Inst,e Projectos Industriais"],
                ["Agentes Autónomos e Sistemas Multiagente (SM)", "Agentes Autónomos e Sistemas Multi-Agente"],
                ["Gestão de Redes e Sistemas Distribuídos", "Gestão de Redes e Sistemas Distribuídos /  Gestão de Redes e Serviços", "Gestão de Redes e Serviços"],
                ["Sistemas de Apoio à Decisão", "Sistemas de Apoio Á Decisão (SIE)"],
                ["Trabalho Final de Curso I", "Trabalho Final de Curso I (Leic)"],
                ["Análise Matemática I - 2ª Fase", "Análise Matemática I", "Análise Matemática I A"],
                ["Análise Matemática II", "Análise Matemática II A"],
                ["Análise Matemática III", "Análise Matemática III A"],
                ["Análise Matemática IV", "Análise Matemática IV A"],
                ["Arquitectura Tecnológica dos Sistemas de Informação", "Arquitectura Tecnológica de Sistemas de Informação Empresariais"],
                ["Análise e Síntese de Algoritmos", "Análise e Sintese de Algoritmos"],
                ["Redes de Computadores", "Redes de Computadores I", "Redes de Computadores I / Redes de Computadores"],
                ["Sistemas Distribuidos", "Sistemas Distribuídos"],
                ["Desenho Técnico I", "Desenho Técnico I/Desenho I"],
                ["Engenharia de Materiais/Materiais", "Engenharia de Materiais"],
                ["Fundamentos de Gestão", "Fundamentos de Gestao", "Fundamentos de Gestao/Economia II"],
                ["Física II/Electro. e Óptica/Termo. e Est. da Matéria", "Termodinâmica e Estrutura da Matéria"],
                ["Máquinas e Sistemas Marítimos II", "Máquinas e Sistemas Marítimos II/Máquinas e Sistemas Marítimos III"],
                ["Química/Química Geral", "Química Geral", "Química"],
                ["Hidráulica", "Hidráulica/Mecânica dos Fluidos e Hidráulica"],
                ["Introdução à Investigação em Engenharia Electrotécnica e de Computadores", "Introdução à Investigação e ao Projecto em Engenharia Electrotécnica e de Computadore"],
                ["Design of Robust Multivariable Feedback Control Systems" , "Design of Robust Multivariable Feedback Control Systems MD"],
                ["Dynamic Stochastic Estimation, Prediction and Smoothing", "Dynamic Stochastic Estimation, Prediction and Smoothing MD"],
                ["Análise de Sistemas Aplicada Á Gestão Costeira", "Análise de Sistemas Aplicada à Gestão Costeira"],
                ["Gestão e Ordenamento de Recursos Litorais", "Gestão e Ordenamento de Sistemas Litorais"],
                ["Modelação de Fenómenos de Transportes e da Qualidade da Água", "Modelação de Fenómenos de Transporte e da Qualidade da Água"],
                ["Introdução a Metodologias de Investigação Sócio-Económica", "Introdução a Metodologias de Investigação Socio-Económica"],
                ["Aspectos de Química de Elementos e Compostos no Ambiente. Toxicidade e Poluição", "Aspectos de Quimica de Elementos e Compostos no Ambiente. Toxicidade e Poluição", "Aspectos da Química de Produtos Naturais, Poluentes e Toxicologia"],
                ["Ensaios Específicos e Imunológicos em Análise Química", "Ensaios Específicos e Imunológicos em Análise Química. Análise Sensorial"],
                ["Economia e Planeamento dos Eventos e Atracções Turísticas", "Economia e Planeamento dos Eventos e Atracções Turisticas"],
                ["Diagnóstico e Conservação de Estradas e Obras de Arte" , "Diagnóstico e Manutenção de Estradas e Obras de Arte"],
                ["Projectos de Infraestruturas Urbanas I", "Projecto de Infraestruturas Urbanas I"],
                ["Estudos de Ciência:Arte,Tecnologia e Sociedade", "Estudos de Ciência: Arte, Tecnologia e Sociedade"],
                ["Estudos de Impacto Ambiental/Impactes Ambientais", "Estudos de Impacto Ambiental", "Impactes Ambientais", "Ambientes e Impactes", "Ambientes e Impactes /  Ambiente Urbano e Espaço Construído"],
                ["Introdução à Arquitectura e ao Projecto", "Introdução à Arquitectura"],
                ["Reabilitação de Construções - Estudo de Casos", "Reabilitação de Construções- Estudo de Casos", "Reabilitação de Construções. Estudos de Caso"],
                ["Tecnologias de Instalações e Equipamentos Prediais" , "Tecnologia de Instalações e Equipamentos Prediais"],
                ["Elementos de Criptografia", "Criptografia e Protocolos de Segurança", "Elementos de Criptografia /  Criptografia e Protocolos de Segurança"],
                ["Desenho", "Desenho I"],
                ["Dissertação de Mestrado em Engª Física Tecnológica", "Dissertação de Mestrado em Engenharia Física Tecnológica"],
                ["Economia do Ambiente", "Economia do Ambiente / Economia, Energia e Ambiente"],
                ["Sistemas de Informação Geográfica e Bases de Dados", "Sistemas de Informação Geográfica"],
                ["Laboratório de Química Geral I", "Laboratório de Química Geral"],
                ["Monitorização e Controlo de Bioprocessos", "Monitorização e Controlo de Bio Processos"],
                ["Química Bioinorgânica", "Química Bio Inorgânica"],
                ["Química-Física", "Química-Física I", " Química-Física / Química-Física I", "Química Física"],
                ["Instalações,Serviços Industriais e Segurança", "Instalações, Serviços Industriais e Segurança"],
                ["Bioquímica e Biologia Molecular", "Biologia Celular e Molecular/Bioquimica e Biologia Molecular"],
                ["Fisiologia de Sistemas" , "Fisiologia de Sistemas I"],
                ["Dinâmica das Rochas/Dinâmica dos Solos e das Rochas", "Dinâmica dos Solos e Rochas", "Dinâmica das Rochas"],
                ["Urbanística ? História e Teorias da Cidade", "Urbanística, História e Teorias da Cidade"]
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
                                    if 'caracter público' in qucPage:
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
                                            evaluationType = "Avaliação dos QUC\n"
                                            if 'Docente:' in page:
                                                beautifulSoupPage = BeautifulSoup(page, "html.parser")
                                                teacher = beautifulSoupPage.body.find_all('p')
                                                for tag in teacher:
                                                    if 'Docente:' in str(tag):
                                                        teacherName = re.findall(r'<b>(.*?)</b>',str(tag),re.DOTALL)
                                                qucFile = open(qucPath + "\\" + "quc" + " " + newKey + ".txt", "a", encoding="utf-8")
                                                evaluationType = "Avaliação dos QUC do professor " + teacherName[0] + "\n"
                                            else:
                                                if webDegreeAcronym[0] not in degreeAcronym:
                                                    continue                                                
                                                qucFile = open(qucPath + "\\" + "quc" + " " + newKey + ".txt", "w", encoding="utf-8")
                                                for row in approvals:
                                                    qucFile = open(qucPath + "\\" + "quc" + " " + newKey + ".txt", "a", encoding="utf-8")
                                                    if 'Taxa de aprovação' in row:    
                                                        parseQucInfo(qucFile, "Taxa de aprovação\n", row)
                                                    if 'Média classificações' in row:
                                                        parseQucInfo(qucFile, "Média das notas dos alunos\n", row)
                                            if parsedPage:
                                                qucFile.write(evaluationType)
                                                parseQucEvaluationInfo(qucFile, parsedPage)
                                            if 'e Tipo de aula:' in page:
                                                teacherEvaluation = re.findall(r'e Tipo de aula:(.*?)</div>',page,re.DOTALL)
                                                teacherEvaluation = teacherEvaluation[0].replace('\n', '')
                                                teacherEvaluation = teacherEvaluation.replace('\t', '')
                                                qucFile.write("Avaliação do professor " + teacherName[0] + "\n")
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
    guiWindow.title("TécnicoVis Login")
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
                                        splittedDegreeName, coursePath = findPath(degreeName.lower().split('ciências de engenharia - ', 1)[1], degreeAcronym, path, newYear)
                                    except IndexError:
                                        splittedDegreeName, coursePath = findPath(degreeName, degreeAcronym.split('-pB', 1)[0], path, newYear)
                                if not os.path.isfile(coursePath):       
                                    try:
                                        splittedDegreeName, coursePath = findPath(degreeName.lower().split('ciências de engenharia - ', 1)[1], degreeAcronym.split('-pB', 1)[0], path, newYear)
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
                                    courseCompareTerm = courseCompareTerm.replace('º', '')
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
                    formattedAcronym = formattedAcronym.replace('-', '').replace('–', '').replace(' ', '').split("_",1)[0][0:7].upper()
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
                                    evMethod = evMethod.replace("Testes/Exames", '').replace("Exame: Época Especial", '')
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
                            if "Avaliação dos QUC" in line:
                                skip = False
                            if infoToExtract:
                                if "respostas insuficiente" not in line and not skip:
                                    teacherInfo.setdefault(teacherName, []).append(float(line))
                                else:
                                    line = "NULL"
                                    teacherInfo.setdefault(teacherName, []).append(line)
                                infoToExtract = False
                            if 'Avaliação do professor' in str(line):
                                teacherName = line.split('Avaliação do professor ',1)[1]
                                infoToExtract = True  
                                for teacher in courseInfoList["teachers"]:
                                    if teacherName == teacher["name"]:
                                        teacherData[teacherName] = teacher["istId"] 
                if '(ead)' not in courseFullName.lower() and '2ª Fase' not in courseFullName.lower():
                    parsedCourseName = unicodedata.normalize('NFKD', courseFullName).encode('ASCII','ignore').decode('utf-8').split(' (',1)[0].split('(',1)[0].lower()
                acronym = compareAcronym(courseFullName, repeatedAcronym)
                if acronym != '':
                    formattedAcronym = acronym
                else:
                    if formattedAcronym in repeatedAcronym and getCoursePairs(repeatedAcronym[formattedAcronym], parsedCourseName) == False or formattedAcronym == '' or formattedAcronym == '$':
                        courseNameStop = ' '.join(filter(lambda word: word not in stopWords, parsedCourseName.split())).title()
                        formattedAcronym = re.sub('[^A-Z]', '', courseNameStop)
                        formattedAcronym = formattedAcronym.replace('-', '').replace('_', '').replace('–', '').replace(' ', '')[0:7]
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
                if os.path.isfile(qucPath) and 'Dissertação' not in courseFullName:        
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
                            if 'Avaliação dos QUC' == line:
                                infoToExtract = True
                    infoToExtract = False
                    with open(qucPath, encoding="utf8") as file:
                        for line in file:
                            line = line.replace('\n','')                      
                            if infoToExtract:
                                grade = line
                                break
                            if 'Média' in line:
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
    courseFullName = courseFullName.replace("–", "-")
    courseCredits = courses["credits"]
    courseTerm = courses["academicTerm"]
    courseTerm = courseTerm.replace('Semestre ' + key, '').replace('º', '')
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
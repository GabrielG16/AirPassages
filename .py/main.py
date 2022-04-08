from Scraping import pesquisas
import pandas as pd


def run():

    #   cidade_origem = input('Cidade partida: ')
    cidade_origem = 'São Paulo'
    #   cidade_destino = input('Cidade destino: ')
    cidade_destino = 'Maceió'

    #   data_partida = input('Data de partida(dd/mm/yyyy): ')
    data_partida = '27/05/2022'
    #   data_retorno = input('Data de retorno (dd/mm/yyyy): ')
    data_retorno = '02/06/2022'

    results_123 = pesquisas.realiza_pesquisa_123(cidade_origem, cidade_destino, data_partida, data_retorno)
    results_google = pesquisas.realiza_pesquisa_google(cidade_origem, cidade_destino, data_partida, data_retorno)
    apanhado_geral = pd.concat([results_123, results_google], axis=1)
    return apanhado_geral


if __name__ == '__main__':
    run()

import os
import pandas as pd
import concurrent.futures

from constants.brazilian_states import brazilian_states

def filterSpreadsheet(data):
    def filtrarDataframe(data, df):
        def idade(df, desde, ate):
            if desde and ate:
                df = df[(df['idade'] >= desde) & (df['idade'] <= ate)]
            elif desde:
                df = df[df['idade'] >= desde]
            else:
                df = df[df['idade'] <= ate]
            return df

        def parcela(df, desde, ate):
            if desde and ate:
                df = df[(df['parcela'] >= desde) & (df['parcela'] <= ate)]
            elif desde:
                df = df[df['parcela'] >= desde]
            else:
                df = df[df['parcela'] <= ate]
            return df

        def soma_parcela(df, desde, ate):
            if desde and ate:
                df = df[(df['soma parcela'] >= desde)
                        & (df['soma parcela'] <= ate)]
            elif desde:
                df = df[df['soma parcela'] >= desde]
            else:
                df = df[df['soma parcela'] <= ate]
            return df

        def esp(df, arrayEsp):
            df = df[df['esp'].isin(arrayEsp)]
            return df

        def banco_emp(df, arrayBancos):
            df = df[df['banco emp'].isin(arrayBancos)]
            return df

        def banco_pgto(df, arrayBancos):
            df = df[df['banco PGTO'].isin(arrayBancos)]
            return df

        print('start filtering')

        df[['parcela', 'soma parcela', 'juros']] = df[['parcela', 'soma parcela',
                                                       'juros']].apply(lambda x: x.str.replace(',', '.').astype(float))

        # line above for
        # df['parcela'] = df['parcela'].str.replace(',', '.')
        # df['parcela'] = df['parcela'].astype(float)
        # df['soma parcela'] = df['soma parcela'].str.replace(',', '.')
        # df['soma parcela'] = df['soma parcela'].astype(float)
        # df['juros'] = df['juros'].str.replace(',', '.')
        # df['juros'] = df['juros'].astype(float)

        if data['idade']['min'] or data['idade']['max']:
            df = idade(df, data['idade']['min'], data['idade']['max'])

        if df.empty:
            return df

        if data['parcela']['min'] or data['parcela']['max']:
            df = parcela(df, data['parcela']['min'], data['parcela']['max'])

        if df.empty:
            return df

        if data['soma_parcela']['min'] or data['soma_parcela']['max']:
            df = soma_parcela(df, data['soma_parcela']['min'],
                              data['soma_parcela']['max'])

        if df.empty:
            return df

        if data['esp']:
            df = esp(df, data['esp'])

        if df.empty:
            return df

        if data['banco_emp']:
            df = banco_emp(df, data['banco_emp'])

        if df.empty:
            return df

        if data['banco_pgto']:
            df = banco_pgto(df, data['banco_pgto'])

        print(df)

        return df

    def get_optimal_chunksize(file_path, memory_limit):
        file_size = os.path.getsize(file_path)
        buffer_size = 70000  # You can adjust this as needed - default: 100000
        chunksize = (file_size / memory_limit) * buffer_size
        return int(chunksize)
    
    arquivos_planilha = []

    for uf in data['uf']:
        if uf in brazilian_states:
            arquivos_planilha.append('csv/' + uf + '.csv')

    if arquivos_planilha == []:
        return []

    dfs = []
    for arquivo in arquivos_planilha:
        print('LOADING CSV: ', arquivo)

        # Usamos o ponto e vírgula como delimitador
        df = pd.read_csv(arquivo, delimiter=';',
                         chunksize=get_optimal_chunksize(arquivo, 100000000))
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = []

            futures.extend(executor.submit(filtrarDataframe, data, chunk)
                           for chunk in df)
            for future in concurrent.futures.as_completed(futures):
                dfs.append(future.result())

            executor.shutdown(wait=True)

        dados_combinados = pd.concat(dfs, ignore_index=True)
        dados_combinados.to_csv('planilha_combinada.csv', index=False)
        returnData = dados_combinados.to_dict(orient='records')

        return returnData

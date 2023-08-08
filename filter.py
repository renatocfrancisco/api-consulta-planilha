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

        df[['parcela', 'soma parcela', 'juros']] = df[['parcela', 'soma parcela',
                                                       'juros']].apply(lambda x: x.str.replace(',', '.').astype(float))

        conditions = [
            (data['idade']['min'] or data['idade']['max'], idade,
             (data['idade']['min'], data['idade']['max'])),
            (data['parcela']['min'] or data['parcela']['max'], parcela,
             (data['parcela']['min'], data['parcela']['max'])),
            (data['soma_parcela']['min'] or data['soma_parcela']['max'], soma_parcela,
             (data['soma_parcela']['min'], data['soma_parcela']['max'])),
            (data['esp'], esp, (data['esp'],)),
            (data['banco_emp'], banco_emp, (data['banco_emp'],)),
            (data['banco_pgto'], banco_pgto, (data['banco_pgto'],))
        ]

        for condition, func, args in conditions:
            if condition:
                df = func(df, *args)
                if df.empty:
                    return df

        return df

    def get_optimal_chunksize(file_path, memory_limit):
        file_size = os.path.getsize(file_path)
        buffer_size = 70000  # default: 100000
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
    returnData = dados_combinados.to_csv(index=False)

    return returnData

import json
import time
import pandas as pd
import concurrent.futures

chunkSizeFiles = {
    'csv/SP.csv': 70000,
    'csv/TO.csv': 50000,
}


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


with open('data.json') as f:
    data = json.load(f)
    print('data.json loaded')

# start timer
start = time.time()

dfs = []
chunksize = 80000
arquivos_planilha = ['csv/SP.csv', 'csv/TO.csv']
for arquivo in arquivos_planilha:
    print('LOADING CSV: ', arquivo)

    # check if chunkSizeFiles[arquivo] is defined
    if arquivo not in chunkSizeFiles:
        continue

    # Usamos o ponto e vírgula como delimitador
    df = pd.read_csv(arquivo, delimiter=';', chunksize=chunkSizeFiles[arquivo])
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = []

        futures.extend(executor.submit(filtrarDataframe, data, chunk)
                       for chunk in df)
        for future in concurrent.futures.as_completed(futures):
            dfs.append(future.result())

        # for chunk in df:
        #     if chunk.empty:
        #         continue

        #     futures.extend([executor.submit(filtrarDataframe, data, chunk)])
        #     for future in concurrent.futures.as_completed(futures):
        #         dfs.append(future.result())

            # df_filtrado = filtrarDataframe(data, chunk)
            # dfs.append(df_filtrado))

        executor.shutdown(wait=True)

dados_combinados = pd.concat(dfs, ignore_index=True)
dados_combinados.to_csv('planilha_combinada.csv', index=False)
print(dados_combinados)

# filtrarDataframe(data, df)

# end timer
end = time.time()
print('time: ', end - start)

# output to csv
# df.to_csv('output.csv', index=False)

# output to dict
# returnData = df.to_dict(orient='records')
# print(returnData)

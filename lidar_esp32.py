import pathlib
import socket
import traceback
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

while True:
    df = pd.DataFrame(columns=['x', 'y', 'z', 's'])

    sel = input("Realizar leitura de arquivos ou scan? [f|s]\nPara sair digite 'q': ")
    if sel.lower() == 'f':
        paths=[]
        search = pathlib.Path(pathlib.Path().resolve())
        for item in search.iterdir():
            if item.is_file():
                if item.name.split('.')[1] == 'csv':
                    paths.append(item)

        if len(paths) <= 0:
            print('Nenhum arquivo encontrado...')
            continue

        print([f'{paths.index(x)} - {x}' for x in paths])
        fname = int(input("Escolha o arquivo: "))
        while fname >= len(paths):
            fname = int(input(f"Existem apenas {len(paths)} arquivo(s). Escolha um deles: "))
        selPath = paths[fname]
        csv_df = pd.read_csv(selPath, delimiter=',')
        print(f"Carregando {selPath}... ")

        for i, rows in csv_df.iterrows():
            dist = float(rows[2])
            strength = float(rows[3])
            x = float(rows[4])
            y = float(rows[5])
            z = float(rows[6])
            if dist <= 1200 or dist <= 0:
                if strength <= 20000.0:
                    dftemp = {'x': x, 'y': y, 'z': z, 's': strength}
                    df.loc[len(df)] = dftemp

    elif sel.lower() == 's':
        host = socket.gethostbyname(socket.gethostname())
        port = 8090

        s = socket.socket()
        s.bind((host, port))
        s.listen(0)

        print("Buscando pelo Client")
        client, addr = s.accept()
        print("Client conectado!")

        scan_df = pd.DataFrame(columns=["horizontal", "vertical", "depth", "strength", "x", "y", "z"])
        print("Escaneando...")

        longSet = []
        while True:
            raw = client.recv(1024)
            try:
                data = raw.decode('utf-8').split('|')
                for x in data:
                    if len(x) > 0:
                        print(x)
                        longSet.append(x)

                if len(raw) == 0:
                    print("Scan finalizado!")
                    break

            except Exception as err:
                print(err)
                traceback.print_exc()

        client.close()
        s.close()

        print("Calculando resultado...")
        for e in longSet:
            try:
                bites = str(e).split(",")
                x = float(bites[2]) * np.cos(np.deg2rad(float(bites[1]))) * np.cos(np.deg2rad(float(bites[0])))
                y = float(bites[2]) * np.sin(np.deg2rad(float(bites[1]))) * np.cos(np.deg2rad(float(bites[0])))
                z = float(bites[2]) * np.sin(np.deg2rad(float(bites[0])))

                scan_df.loc[len(scan_df)] = [bites[0], bites[1], bites[2], bites[3], x, y, z]

                if float(bites[2]) <= 1200 or float(bites[2]) == 0:
                    if float(bites[3]) <= 20000.0:
                        dftemp = {'x': x, 'y': y, 'z': z, 's': float(bites[3])}
                        df.loc[len(df)] = dftemp
                        if len(df) % 100 == 0:
                            continue
            except Exception as e:
                print(f"Erro, {e}")
                traceback.print_exc()

        # Salvando CSV
        path = f"Lidar {datetime.strftime(datetime.now(), '%d_%m_%Y %H_%M_%S')}.csv"
        print(f'Criando arquivo csv: {path}')
        scan_df.to_csv(path, index=False)

        print("Fim.")
    elif sel == 'q':
        exit(0)
    else:
        print('Input inválido, tente novamente.')
        continue

    print("Abrindo gráfico de dispersão...")

    # Plotagem 3D
    x = df['x']
    y = df['y']
    z = df['z']
    s = df['s']

    trace1 = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(
            size=10,
            color=s,
            colorscale='Viridis',
            opacity=0.7))
    data = [trace1]
    layout = go.Layout(
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0)
    )
    fig = go.Figure(data=data, layout=layout)
    fig.show()

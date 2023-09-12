import socket
import csv
import datetime
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import os
import time


def map(x, inmin, inmax, outmin, outmax):
    return int((x - inmin) * (outmax - outmin) / (inmax - inmin) + outmin)


while True:
    c = input("Realizar leitura de arquivos ou scan? [f|s]\nPara sair digite 'q': ")
    df = pd.DataFrame(columns=['x', 'y', 'z', 's'])

    if c == 'f':
        paths = []
        selPath = ""
        c = 0
        for root, dirs, files in os.walk("."):
            for file in files:
                if file.endswith(".csv"):
                    print(str(c) + ": " + os.path.join(root, file))
                    paths.append(os.path.join(root, file))
                    c += 1
        c = int(input("Escolha o arquivo: "))

        while c >= len(paths):
            c = int(input(f"Existem apenas {len(paths)} arquivo(s). Escolha um deles: "))
        selPath = str(paths[c]).replace('.\\', '')
        print(f"Carregando {selPath}...")

        rows=0
        with open(selPath) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            rows = int(len(list(readCSV)))
            print("Linhas: " + str(rows))

        barSize = 50
        with open(selPath) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            next(readCSV)

            c=0
            for row in readCSV:
                dist = float(row[2])
                strength = float(row[3])
                x = float(row[4])
                y = float(row[5])
                z = float(row[6])
                if dist <= 1200 or dist <= 0:
                    if strength <= 20000.0:
                        dftemp = {'x': x, 'y': y, 'z': z, 's': strength}
                        df = df.append(dftemp, ignore_index=True)
                        print(
                            str(float(row[0])) + "," + str(float(row[1])) + "," + str(dist) + "," + str(strength) + "|")

        print("\n")

    elif c == 's':
        host = socket.gethostbyname(socket.gethostname())
        port = 8090

        s = socket.socket()
        s.bind((host, port))
        s.listen(0)

        # get time and date
        timestamp = datetime.datetime.now()

        # create CSV
        path = str(timestamp.day) + "-" + str(timestamp.month) + "-" + str(timestamp.year) + "_" + str(
            timestamp.hour) + "-" + str(timestamp.minute) + "-" + str(timestamp.second) + ".csv"
        print(path)

        print("Buscando pelo Client")
        (client, addr) = s.accept()
        print("\rClient conectado!")

        file = open(path, 'w', encoding='UTF8', newline='')
        writer = csv.writer(file)
        writer.writerow(["horizontal", "vertical", "depth", "strength", "x", "y", "z"])

        longSet = []
        final = []

        print("Escaneando...")
        while True:
            raw = client.recv(64)
            longSet.append(raw.decode('utf-8'))

            if len(raw) == 0:
                print("Pronto!")
                break

        client.close()
        s.close()
        print("Calculando resultado...")
        final = str("".join(longSet)).split("|")
        for e in final:
            try:
                bites = str(e).split(",")
                x = float(bites[2]) * np.cos(np.deg2rad(float(bites[1]))) * np.cos(np.deg2rad(float(bites[0])))
                y = float(bites[2]) * np.sin(np.deg2rad(float(bites[1]))) * np.cos(np.deg2rad(float(bites[0])))
                z = float(bites[2]) * np.sin(np.deg2rad(float(bites[0])))

                writer.writerow([bites[0], bites[1], bites[2], bites[3], x, y, z])
                if float(bites[2]) <= 1200 or float(bites[2]) == 0:
                    if float(bites[3]) <= 20000.0:
                        dftemp = {'x': x, 'y': y, 'z': z, 's': float(bites[3])}
                        df = df.append(dftemp, ignore_index=True)

                        if len(df) % 100 == 0:
                            # loading(c)
                            if c == 4:
                                c = 0
                            else:
                                c += 1
            except Exception as e:
                print(f"Erro, {e}")

        print("Fim.")

        file.close()
    elif c == 'q':
        exit(0)
    else:
        print("Input inválido. Encerrando...")
        exit(0)

    print("Abrindo gráfico de dispersão...")

    ##3d Plot
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

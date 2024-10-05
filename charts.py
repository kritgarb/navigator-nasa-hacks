import plotly.graph_objects as go
import query as q
import similarity as s

def create_chart():
  import plotly.graph_objects as go
import query as q
import similarity as s

# Fazendo a requisição
df = q.make_request()

if df is not None:
    # Filtrando dados para garantir que todos os planetas tenham massa, raio, distância, densidade e gravidade conhecidos
    df = df.dropna(subset=['pl_bmasse', 'pl_rade', 'sy_dist_pc', 'density', 'gravity'])

    # Verificando se há dados após a filtragem
    print(f"Número de planetas filtrados: {len(df)}")

    if len(df) == 0:
        print("Nenhum dado disponível para visualização.")
    else:
        # Criando listas para armazenar os dados
        planets = df['pl_name'].tolist()  # Lista com os nomes dos planetas
        distance_from_earth = df['sy_dist_pc'].tolist()  # Usando a distância em parsecs
        planet_diameter = (df['pl_rade'] * 2).astype(float).tolist()  # Diâmetro como duas vezes o raio
        density = df['density'].tolist()
        gravity = df['gravity'].tolist()
        temperature = df['pl_eqt'].tolist()  # Temperatura do planeta

        # Calculando a habitabilidade
        habitability_scores = [s.calculate_habitability(temp, dens, grav) for temp, dens, grav in zip(temperature, density, gravity)]

        # Garantindo que o tamanho das bolhas esteja correto ajustando o 'sizeref'
        sizeref_value = max(planet_diameter) / 30  # Ajustar para que o tamanho das bolhas fique visível

        # Criar a anotação no hover com nome do planeta, distância, densidade, gravidade e percentual de habitabilidade
        hover_text = []
        for i in range(len(planets)):
            hover_text.append(f"Planet: {planets[i]}<br>"
                              f"Distance: {distance_from_earth[i]:.2f} pc<br>"
                              f"Density: {density[i]:.2f} kg/m³<br>"
                              f"Gravity: {gravity[i]:.2f} m/s²<br>"
                              f"Habitability Score: {habitability_scores[i]}%")

        # Criar traço, dimensionando as bolhas pelo diâmetro do planeta
        fig = go.Figure(data=go.Scatter3d(
            x=distance_from_earth,
            y=density,   # Densidade
            z=gravity,    # Gravidade
            text=hover_text,  # Mostra informações detalhadas no hover
            mode='markers',
            marker=dict(
                sizemode='diameter',
                sizeref=sizeref_value,  # Ajustado para melhorar a visibilidade das bolhas
                size=planet_diameter,
                color=habitability_scores,  # Colorindo com base na pontuação de habitabilidade
                colorbar_title='Habitability Score (%)',  # Título para a barra de cores
                colorscale=[[0, 'rgb(178, 10, 28)'], [1, 'rgb(5, 10, 172)']],
                opacity=1  # Tornar as bolhas completamente visíveis (sem transparência)
            ),
            hoverinfo="text"  # Exibe o conteúdo do hover_text
        ))

        # Atualizando o layout do gráfico para fundo preto e linhas dos eixos visíveis
        fig.update_layout(
            scene=dict(
                xaxis=dict(
                    title='Distance from Earth (Parsecs)',
                    titlefont_color='white',
                    showbackground=True,
                    backgroundcolor='black',  # Fundo preto
                    gridcolor='gray',         # Linhas dos eixos em cinza
                    zerolinecolor='white',     # Linha do zero em branco
                    color='white'              # Cor do texto dos eixos
                ),
                yaxis=dict(
                    title='Density (kg/m³)',
                    titlefont_color='white',
                    showbackground=True,
                    backgroundcolor='black',  # Fundo preto
                    gridcolor='gray',         # Linhas dos eixos em cinza
                    zerolinecolor='white',     # Linha do zero em branco
                    color='white'              # Cor do texto dos eixos
                ),
                zaxis=dict(
                    title='Gravity (m/s²)',
                    titlefont_color='white',
                    showbackground=True,
                    backgroundcolor='black',  # Fundo preto
                    gridcolor='gray',         # Linhas dos eixos em cinza
                    zerolinecolor='white',     # Linha do zero em branco
                    color='white'              # Cor do texto dos eixos
                ),
                bgcolor='black'  # Fundo geral do gráfico preto
            ),
            paper_bgcolor='black',  # Fundo fora do gráfico (site) preto
            plot_bgcolor='black'    # Fundo dentro do gráfico preto
        )

        # Mostrar o gráfico
        fig.show()

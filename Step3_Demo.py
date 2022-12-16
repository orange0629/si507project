import flask, json, random
from demo_support import nearest_neighbor, node_to_node, similar_list, rest_stat_dist, valid_rest_id
import plotly.graph_objs as go

from flask import Flask, render_template, request, redirect
app = Flask(__name__)



@app.route('/')
def index():
    rest_list = []
    for i in range(100):
        rest_list.append(rest[str(random.randint(0,970))])
    return render_template('index.html', rest_list = rest_list)

@app.route('/neighbor', methods=['GET', 'POST'])
def neighbor_form():
    if flask.request.method == 'POST':
        node = request.form["node"]
        return redirect("/neighbor/" + node, code=302)
    else:
        return render_template('rest_neighbor.html', init_node = [], rest_list = [])

@app.route('/neighbor/<node>')
def rest_neighbor(node):
    if valid_rest_id(node, rest):
        rest_old = nearest_neighbor(graph_dict, node, 100)
        rest_new = []
        for step in rest_old:
            rest_new.append([rest[step[0]], step[1]])
        return render_template('rest_neighbor.html', init_node = rest[node], rest_list = rest_new)
    else:
        return "Check your input!"


@app.route('/path/<node1>/<node2>')
def rest_path(node1, node2):
    if valid_rest_id(node1, rest) and valid_rest_id(node2, rest):
        path_old = node_to_node(graph_dict, node1, node2)
        path_new = []
        for step in path_old:
            path_new.append([rest[step[0]], step[1]])
        return render_template('rest_path.html', init_node = rest[node1], path = path_new)
    else:
        return "Check your input!"

@app.route('/path', methods=['GET', 'POST'])
def path_form():
    if flask.request.method == 'POST':
        node1 = request.form["node1"]
        node2 = request.form["node2"]
        return redirect("/path/" + node1 + "/" + node2, code=302)
    else:
         return render_template('rest_path.html', init_node = [], path = [])


@app.route('/similar', methods=['GET', 'POST'])
def similar_form():
    if flask.request.method == 'POST':
        nodes = request.form["nodes"]
        node_list = nodes.replace(' ', '').split(",")
        rest_old =  similar_list(graph_dict, node_list)
        rest_new = []
        for step in rest_old:
            rest_new.append([rest[step[1]], step[0]])
        return render_template('rest_similar.html', node_list = node_list, rest_list = rest_new)
    else:
        return render_template('rest_similar.html', node_list = [], rest_list = [])



@app.route('/stat', methods=['GET', 'POST'])
def stat_form():
    if flask.request.method == 'POST':
        cuisine = request.form["cuisine"].lower()
        node_list = []

        for node in rest:
            for tag in rest[node]['cuisine']:
                if tag.lower() == cuisine:
                    node_list.append(str(rest[node]['id']))
                    break

        fig_list = []

        plot_x, plot_y = rest_stat_dist(rest, graph_dict, node_list, "Neighborhood")
        fig_list.append(go.Figure(data = go.Bar(x=plot_x, y=plot_y)).to_html(full_html=False))

        
        plot_x, plot_y = rest_stat_dist(rest, graph_dict, node_list, "tags")
        fig_list.append(go.Figure(data = go.Bar(x=plot_x, y=plot_y)).to_html(full_html=False))

        plot_x, plot_y = rest_stat_dist(rest, graph_dict, node_list, "Rating")
        fig_list.append(go.Figure(data = go.Bar(x=plot_x, y=plot_y)).to_html(full_html=False))

        plot_x, plot_y = rest_stat_dist(rest, graph_dict, node_list, "Price_high")
        fig_list.append(go.Figure(data = go.Bar(x=plot_x, y=plot_y)).to_html(full_html=False))
        
        return render_template('rest_stat.html', fig_list = fig_list, cuisine = request.form["cuisine"])
    else:
        return render_template('rest_stat.html', fig_list = [], cuisine = [])

if __name__=='__main__':
    cache_file = open('graph_dict.json', 'r')
    cache_content = cache_file.read()
    graph_dict = json.loads(cache_content)
    cache_file.close()

    cache_file = open('restaurants.json', 'r')
    cache_content = cache_file.read()
    rest = json.loads(cache_content)
    cache_file.close()

    print('Starting Flask app', app.name)
    app.run(debug=True)
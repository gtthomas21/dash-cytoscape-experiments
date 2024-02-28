from dash import Dash, html, dcc, Input, Output, callback
import dash_cytoscape as cyto
import random

app = Dash(__name__)

new_node_id_counter = 0  # Global counter to ensure unique IDs for new nodes

nodes = [
    {
        'data': {'id': short, 'label': label, 'hyper_link': city_link},
        'position': {'x': 20*lat, 'y': -20*long},
        'classes': node_class,
    }
    for short, label, long, lat, node_class, city_link in (
        ('la', 'Los Angeles', 34.03, -118.25, 'unselected', 'https://www.timeout.com/los-angeles/things-to-do/los-angeles-attractions'),
        ('nyc', 'New York', 40.71, -74, 'unselected', 'https://www.newyorker.com/magazine/2011/02/07/show-the-monster'),
        ('to', 'Toronto', 43.65, -79.38, 'unselected', 'https://en.wikipedia.org/wiki/Toronto'),
        ('mtl', 'Montreal', 45.50, -73.57, 'unselected', 'https://en.wikipedia.org/wiki/Montreal'),
        ('van', 'Vancouver', 49.28, -123.12, 'unselected', 'https://en.wikipedia.org/wiki/Vancouver'),
        ('chi', 'Chicago', 41.88, -87.63, 'unselected', 'https://en.wikipedia.org/wiki/Chicago'),
        ('bos', 'Boston', 42.36, -71.06, 'unselected', 'https://en.wikipedia.org/wiki/Boston'),
        ('hou', 'Houston', 29.76, -95.37, 'unselected', 'https://en.wikipedia.org/wiki/Houston')
    )
]

edges = [
    {'data': {'source': source, 'target': target}}
    for source, target in (
        ('van', 'la'),
        ('la', 'chi'),
        ('hou', 'chi'),
        ('to', 'mtl'),
        ('mtl', 'bos'),
        ('nyc', 'bos'),
        ('to', 'hou'),
        ('to', 'nyc'),
        ('la', 'nyc'),
        ('nyc', 'bos')
    )
]

elements = nodes + edges

default_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'background-color': '#BFD7B5',
            'label': 'data(label)'
        }
    },
    {
        'selector': ".selected",
        'style': {
            'background-color': 'red'
        }
    },
    {
        'selector': ".unselected",
        'style': {
            'background-color': '#BFD7B5'
        }
    },
    {
        'selector': 'edge',
        'style': {
            'line-color': '#A3C4BC'
        }
    },
]


app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-stylesheet-callbacks',
        layout={'name': 'preset'}, # <--- 'layout' 'cose' would make the graph remake itself on callback
        elements=elements,
        stylesheet=default_stylesheet,
        style={'width': '100%', 'height': '450px'}
    ),
    html.P(id='weird_callback_attempt', children=[
        html.P(children="Some text"),
        html.A(id='cytoscape-tapNodeData-output', href='', children='City Link!'),
    ]),
    # html.A(id='cytoscape-tapNodeData-output', href='', children='City Link!'),
    html.P(id='cytoscape-tapEdgeData-output'),
])


@callback(Output('cytoscape-stylesheet-callbacks', 'elements'),
          [Input('cytoscape-stylesheet-callbacks', 'tapNodeData')])
def update_node_style_on_click(data):
    global new_node_id_counter  # Use the global counter to keep track of new node IDs
    global elements

    if not data:
        return elements  # Return the original elements if no node data is provided

    clicked_node_id = data['id']

    # Generate a new node ID and label
    new_node_id = f"new_{new_node_id_counter}"
    new_node_label = f"New Node: {new_node_id}"
    new_node_id_counter += 1  # Increment the counter for the next new node

    # Generate random positions for the new node
    new_node_x = random.randint(30, 50)
    new_node_y = random.randint(70, 125)

    # Define the new node
    new_node = {
        'data': {'id': new_node_id, 'label': new_node_label},
        'position': {'x': new_node_x, 'y': new_node_y},
        'classes': 'unselected',
    }

    # Create a copy of the current elements and add the new node
    elements = elements[:] + [new_node]

    print(elements)

    return elements

    # # Iterate over the elements to update the 'classes' property of the clicked node
    # updated_elements = []
    # for element in elements:
    #     # Check if the element is the clicked node by ID
    #     if element.get('data', {}).get('id') == clicked_node_id:
    #         # Update 'classes' property to 'selected'
    #         updated_element = {**element, 'classes': 'selected'}
    #     else:
    #         # Keep other elements unchanged
    #         updated_element = element
    #     updated_elements.append(updated_element)
    # print(updated_elements)
    # return updated_elements

@callback(Output('cytoscape-tapNodeData-output', 'href'),
              Input('cytoscape-stylesheet-callbacks', 'tapNodeData'))
def displayTapNodeData(data):
    if data:
        return data['hyper_link']


# @callback(Output(),
#           Input())
# def open_hyperlink(data):



if __name__ == '__main__':
    app.run(debug=True)

# --------------------END OF CODE------------------------

# DONE: 0. Add a side bar (with maybe the name of the node clicked?)
# TODO: 0(b). Stop it reloading the whole graph when the callback is called
#  (e.g. set all the positions based on the old one?) - maybe not top priority
# TODO: 1. Can I have a hyperlink on a node (open a tab on click)
# -// This is actually really difficult to do with Dash / Cytoscape because it is 'server side'
# TODO: 2. Add a 'floating' (i.e. no edges) node on click on a node
# -// did this but it just appears at the far side of the graph. 
# TODO: 3. Add an 'edge' leading back to the node clicked
# TODO: 4. Make some property of the new node (name?) determined by the node you click on
#  e.g. a dictionary depending on the information in that callback as the new node
#  (e.g. 'Los Angeles 2')




# ------------------UNUSED CODE--------------------------

# from dash import Dash, html, Input, Output, callback
# import dash_cytoscape as cyto
#
# app = Dash(__name__)
#
# styles = {
#     'pre': {
#         'border': 'thin lightgrey solid',
#         'overflowX': 'scroll'
#     }
# }
#
#
# nodes = [
#     {
#         'data': {'id': short, 'label': label},
#         'position': {'x': 20*lat, 'y': -20*long}
#     }
#     for short, label, long, lat in (
#         ('la', 'Los Angeles', 34.03, -118.25),
#         ('nyc', 'New York', 40.71, -74),
#         ('to', 'Toronto', 43.65, -79.38),
#         ('mtl', 'Montreal', 45.50, -73.57),
#         ('van', 'Vancouver', 49.28, -123.12),
#         ('chi', 'Chicago', 41.88, -87.63),
#         ('bos', 'Boston', 42.36, -71.06),
#         ('hou', 'Houston', 29.76, -95.37)
#     )
# ]
#
# edges = [
#     {'data': {'source': source, 'target': target}}
#     for source, target in (
#         ('van', 'la'),
#         ('la', 'chi'),
#         ('hou', 'chi'),
#         ('to', 'mtl'),
#         ('mtl', 'bos'),
#         ('nyc', 'bos'),
#         ('to', 'hou'),
#         ('to', 'nyc'),
#         ('la', 'nyc'),
#         ('nyc', 'bos')
#     )
# ]
#
#
# default_stylesheet = [
#     {
#         'selector': 'node',
#         'style': {
#             'background-color': '#BFD7B5',
#             'label': 'data(label)'
#         }
#     }
# ]
#
#
# app.layout = html.Div([
#     cyto.Cytoscape(
#         id='cytoscape-event-callbacks-2',
#         layout={'name': 'preset'},
#         elements=edges+nodes,
#         stylesheet=default_stylesheet,
#         style={'width': '100%', 'height': '450px'}
#     ),
#     html.P(id='cytoscape-tapNodeData-output'),
#     html.P(id='cytoscape-tapEdgeData-output'),
# ])
#
#
# @callback(Output('cytoscape-tapNodeData-output', 'children'),
#               Input('cytoscape-event-callbacks-2', 'tapNodeData'))
# def displayTapNodeData(data):
#     if data:
#         return "You recently clicked/tapped the city: " + data['label']
#
#
# @callback(Output('cytoscape-tapEdgeData-output', 'children'),
#               Input('cytoscape-event-callbacks-2', 'tapEdgeData'))
# def displayTapEdgeData(data):
#     if data:
#         return "You recently clicked/tapped the edge between " + \
#                data['source'].upper() + " and " + data['target'].upper()
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
#
#
# # How do you style a specific node?

# @callback(Output('cytoscape-stylesheet-callbacks', 'stylesheet'),
#               Input('input-line-color', 'value'),
#                Input('input-bg-color', 'value'))
# def update_stylesheet(line_color, bg_color):
#     if line_color is None:
#         line_color = 'transparent'
#
#     if bg_color is None:
#         bg_color = 'transparent'
#
#     new_styles = [
#         {
#             'selector': 'node',
#             'style': {
#                 'background-color': bg_color
#             }
#         },
#         {
#             'selector': 'edge',
#             'style': {
#                 'line-color': line_color
#             }
#         }
#     ]
#
#     return default_stylesheet + new_styles

from dash import Dash, html, dcc
import dash_cytoscape as cyto
from dash.dependencies import Input, Output
import iGetMusic as iGet

app = Dash(__name__)
server = app.server
cyto.load_extra_layouts()

stylesheet = [
    {
        'selector': 'node',
        'style': {'content': 'data(label)'}
    },
    {
        'selector': '.genre_edge',
        'style': {
            'line-color': 'red'
        }
    },
    {
        'selector': '.genre_node',
        'style': {
            'background-color': 'red',
            'background-opacity': '0.2',
            'shape': 'roundrectangle',
            'width': '100%',
            'height': '100%'
        }
    },
    {
        'selector': '.band_node',
        'style': {
            'background-color': 'slategrey',
            'shape': 'circle',
            'width': '50%',
            'height': '50%'
        }
    }
]

genre_nodes = [
    {
        'data': {'id': id, 'label': name},
        'classes': 'genre_node',
    }
    for id, name in (
        ('mdm', 'Melodic Death Metal'),
        ('prg', 'Progressive Metal'),
        ('bm', 'Black Metal'),
        ('dsbm', 'DSBM'),
        ('bg', 'Blackgaze'),
        ('pbm', 'Post-Black Metal'),
        ('abm', 'Atmospheric Black Metal'),
        ('hm', 'Heavy Metal'),
        ('dm', 'Death Metal'),
        ('gm', 'Groove Metal'),
        ('tm', 'Thrash Metal'),
        ('fm', 'Folk Metal'),
        ('pm', 'Power Metal'),
        ('mc', 'Metalcore'),
        ('dc', 'Deathcore'),
    )
]

microgenre_nodes = [
    {
        'data': {'id': id, 'label': name, 'parent': parent},
        'classes': 'genre_node',
    }
    for id, name, parent in (
        ('vm', '"Viking Metal"', 'mdm'),
    )
]
genre_edges = [
    {
        'data': {'source': source, 'target': target},
        'classes': 'genre_edge'
    }
    for source, target in (
        ('bm', 'dsbm'),
        ('bm', 'bg'),
        ('bm', 'pbm'),
        ('bm', 'abm'),
        ('hm', 'bm'),
        ('dm', 'mdm'),
        ('hm', 'dm')
    )
]

band_edges = [
    {
        'data': {'source': source, 'target': target},
        'classes': 'band_edge'
    }
    for source, target in (
        ('ALC', 'pbm'),
        ('KAK', 'abm'),
        ('BLK', 'prg')
    )
]

band_nodes = [
    {
        'data': {'id': id, 'label': name, 'parent': parent, 'song': song},
        'classes': 'band_node'
    }
    for id, name, parent, song in (
        ('INF', 'In Flames', 'mdm', 'Delight and Angers'),
        ('INS', 'Insomnium', 'mdm', 'Down With The Sun'),
        ('ALC', 'Alcest', 'bg', 'Kodama'),
        ('ULV', 'Ulver', 'bm', 'I Troldskog Faren Vild'),
        ('HFS', 'Harakiri for the Sky', 'pbm', 'Manifesto'),
        ('KAK', 'Kekht Arakh', 'pbm', 'Swordsman'),
        ('MGL', 'MGLA', 'bm', 'Exercises in Futility V'),
        ('MUL', 'My Useless Life', 'dsbm', 'A Desolate Heart'),
        ('SVB', 'Svalbard', 'pbm', 'Listen to Someone'),  # Try not to die until you're dead
        ('ELD', 'Elderwind', 'abm', 'The Magic Of Nature'), # Maybe remove
        ('COF', 'Cult of Fire', 'abm', 'Kali Ma'), # Maybe remove
        ('BSB', 'Black Sabbath', 'hm', 'Heaven and Hell'),
        ('ICE', 'Iced Earth', 'hm', 'Anthem'),
        ('DTH', 'Death', 'dm', 'Spirit Crusher'),
        ('AMA', 'Amon Amarth', 'vm', 'Twilight Of The Thunder God'),  # Cry of the Blackbirds
        ('BLK', 'Be\'lakor', 'mdm', 'Abeyance'),  # Root to Sever, Smoke of many fires
        ('SWK', 'Soilwork', 'mdm', 'Distortion Sleep'),
        ('DTQ', 'Dark Tranquility', 'mdm', 'Time out of Place'),
        ('OBC', 'Orbit Culture', 'mdm', 'See Through Me'),
        ('HNT', 'The Haunted', 'mdm', 'The Fallout'),
        ('DIS', 'Disarmonia Mundi', 'mdm', 'Celestial Furnace'),
        ('UTA', 'Unleash the Archers', 'pm', 'Apex'),
        ('TRI', 'Triosphere', 'pm', 'Steal Away the Light'),
        ('ODO', 'Orden Ogan', 'pm', 'Gunman'),
        ('PWF', 'Powerwolf', 'pm', 'Army of the Night'),
        ('OPT', 'Opeth', 'prg', 'Reverie / Harlequin Forest'),
        ('DRT', 'Dream Theatre', 'prg', 'Pull Me Under'),
        ('TVM', 'Trivium', 'mcr', ''),
        ('ALD', 'As I Lay Dying', 'mcr', ''),
        ('LMK', 'Landmvrks', 'mcr', ''),
        ('AVA', 'Aviana', 'mcr', ''),
        ('ALT', 'Allt', 'mcr', ''),
        ('ARC', 'Architects', 'mcr', ''),
        
    )
]
elements = genre_nodes + genre_edges + band_nodes + band_edges + microgenre_nodes
app.layout = html.Div([
    dcc.Location(id="location"),
    cyto.Cytoscape(
        id='cytoscape',
        layout={'name': 'cose-bilkent'},
        style={'width': '100%', 'height': '450px'},
        stylesheet=stylesheet,
        elements=elements
    )
])

@app.callback(
    Output("location", "href"),
    Input("cytoscape", "tapNode"),
    prevent_initial_call=True,
)
def navigate_to_url(node_data):
    match node_data['classes']:
        case 'genre_node':
            return f"https://en.wikipedia.org/wiki/{node_data['data']['label']}"
        case 'band_node':
            return iGet.get(term=f"{node_data['data']['song']} {node_data['data']['label']}", limit=1)[0].getTrackViweUrl()

    
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="8050")
    # app.run(debug=True)

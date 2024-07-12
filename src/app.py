from dash import Dash, html, dcc
import dash_cytoscape as cyto
from dash.dependencies import Input, Output
import iGetMusic as iGet

app = Dash(__name__)
server = app.server
cyto.load_extra_layouts()

# TODO: Button to toggle band edges

stylesheet = [
    {
        'selector': 'node',
        'style': {'content': 'data(label)'}
    },
    {
        'selector': '.genre_edge',
        'style': {
            'line-color': 'slategrey',
            'source-arrow-shape': 'triangle'
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
        ('prg', 'Progressive Metal'),
        ('bm', 'Black Metal'),
        ('hm', 'Heavy Metal'),
        ('dm', 'Death Metal'),
        ('gm', 'Groove Metal'),
        ('tm', 'Thrash Metal'),
        ('fm', 'Folk Metal'),
        ('pm', 'Power Metal'),
        ('mcr', 'Metalcore'),
        ('dcr', 'Deathcore'),
        ('doom', 'Doom Metal'),
        ('goth', 'Gothic Metal'),
        ('crst', 'Crust Punk'),
        ('gcr', 'Grindcore'),
        ('im', 'Industrial Metal'),
        ('sm', 'Symphonic Metal'),
        ('pop', 'Pop Metal'),
        ('hcp', 'Hardcore Punk'),
        ('num', 'Nu Metal'),
        ('alt', 'Alt. Metal'),
              
    )
]

microgenre_nodes = [
    {
        'data': {'id': id, 'label': name, 'parent': parent},
        'classes': 'genre_node',
    }
    for id, name, parent in (
        ('mdm', 'Melodic Death Metal', 'dm'),
        ('vm', '"Viking Metal"', 'mdm'),
        ('pmcr', 'Prog. Metalcore', 'mcr'),
        ('pdcr', 'Prog. Deathcore', 'dcr'),
        ('pmdm', 'Prog. Melodeath', 'mdm'),
        ('ecr', 'Electronicore', 'mcr'),
        ('thl', 'Thall', 'prg'),
        ('celt', '"Celtic Metal"', 'fm'),
        ('pirt', '"Pirate Metal"', 'fm'),
        ('pgm', 'Prog. Groove Metal', 'gm'),
        ('dsbm', 'DSBM', 'bm'),
        ('bg', 'Blackgaze', 'bm'),
        ('abm', 'Atmospheric Black Metal', 'bm'),
        ('bjaz','"Dark Jazz"', 'bm'),
    )
]
genre_edges = [
    {
        'data': {'source': source, 'target': target},
        'classes': 'genre_edge'
    }
    for target, source in (
        ('hm', 'bm'),
        ('hm', 'prg'),
        ('hm', 'im'),
        ('tm', 'dm'),
        ('tm', 'gm'),
        ('hcp', 'dm'),
        ('dm', 'bm'),
        ('bm', 'dm'),
        ('hm', 'pop'),
        ('crst', 'gcr'),
        ('hcp', 'crst'),
        ('hcp', 'mcr'),
        ('hm','mcr'),
        ('hm', 'crst'),
        ('dm','dcr'),
        ('mcr','dcr'),
        ('hm', 'pm'),
        ('hm', 'sm'),
        ('hm', 'goth'),
        ('hm', 'fm'),
        ('hm', 'doom'),
        ('hm', 'tm'),
        ('hm', 'alt'),
        ('im', 'num'),
        
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
        ('HFS', 'Harakiri for the Sky', 'bg', 'Manifesto'),
        ('KAK', 'Kekht Arakh', 'abm', 'Swordsman'),
        ('ELL', 'Ellende', 'abm', 'Wind'),
        ('MGL', 'MGLA', 'bm', 'Exercises in Futility V'),
        ('MUL', 'My Useless Life', 'dsbm', 'A Desolate Heart'),
        ('WHW', 'White Ward', 'bjaz', 'Cronus'),
        ('SVB', 'Svalbard', 'bg', 'Listen to Someone'),  # Try not to die until you're dead
        ('ELD', 'Elderwind', 'abm', 'The Magic Of Nature'), # Maybe remove
        ('COF', 'Cult of Fire', 'abm', 'Kali Ma'), # Maybe remove
        ('BSB', 'Black Sabbath', 'hm', 'Heaven and Hell'),
        ('IRN', 'Iron Maiden', 'hm', 'The Trooper'),
        ('ICE', 'Iced Earth', 'hm', 'Anthem'),
        ('DTH', 'Death', 'dm', 'Spirit Crusher'),
        ('RVC', 'Revocation', 'dm', 'The Grip Tightens'),
        ('AMA', 'Amon Amarth', 'vm', 'Twilight Of The Thunder God'),  # Cry of the Blackbirds
        ('BLK', 'Be\'lakor', 'pmdm', 'Abeyance'),  # Root to Sever, Smoke of many fires
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
        ('DRT', 'Dream Theater', 'prg', 'Pull Me Under'),
        ('TVM', 'Trivium', 'mcr', 'The Sin and the Sentence'),
        ('ALD', 'As I Lay Dying', 'mcr', 'Through Struggle'),
        ('LMK', 'Landmvrks', 'mcr', 'Creature'),
        ('AVA', 'Aviana', 'dcr', 'Oblivion'),
        ('ALT', 'Allt', 'pmcr', 'Remnant'),
        ('ARC', 'Architects', 'mcr', 'Dead Man Talking'),
        ('THN', 'Thornhill', 'mcr', 'Human'),
        ('BRT', 'Bury Tomorow', 'mcr', 'The Agonist'),
        ('MNM', 'Monuments', 'pmcr', 'False Providence'),
        ('ERA', 'ERRA', 'pmcr', 'Nigh to Silence'),
        ('NRT', 'Northlane', 'pmcr', '4D'),
        ('SPB', 'Spiritbox', 'pmcr', 'The Beauty of Suffering'),
        ('INA', 'Invent Animate', 'pmcr', 'Purity Weeps'),
        ('SIP', 'Silent Planet', 'pmcr', 'Second Sun'),
        ('CUR', 'Currents', 'pmcr', 'The Place Where I Feel Safest'),
        ('ECB', 'Electric Callboy', 'ecr', 'Hypa Hypa'),
        ('ESH', 'Enter Shikari', 'ecr', '...Meltdown'),
        ('SLP', 'Slipknot', 'num', 'Wait and Bleed'),
        ('MAC', 'Machine Head', 'num', 'Circle the Drain'),
        ('LIP', 'Linkin Park', 'num', 'Don\'t Stay'),
        ('SOD', 'System of a Down', 'num', 'B.Y.O.B'),
        ('WIT', 'Within Temptation', 'pop', 'Bleed Out'),
        ('BCH', 'Blind Channel', 'pop', 'Flatline'),
        # Bad Omens
        ('BMT', 'Bring Me The Horizon', 'pop', 'Doomed'),
        ('FFA', 'Fit for an Autopsy', 'dcr', 'Two Towers'),
        ('WCH', 'Whitechapel', 'dcr', 'A Bloodsoaked Symphony'),
        ('SOI', 'Shadow of Intent', 'pdcr', 'Intensified Genocide'),
        # ('DWP', 'The Devil Wears Prada', 'mcr', )
        ('HLB', 'Humanity\'s Last Breath', 'pdcr', 'Instill'), # Blackened Deathcore with Thall
        ('VLJ', 'Vildjharta', 'thl', 'lavender haze'),
        ('MIR', 'Mirar', 'thl', 'Franka'),
        ('MGD', 'Megadeth', 'tm', 'The Scorpion'),
        ('MCH', 'Melechech', 'tm', 'Multiple Truths'),  # blackened thrash metal
        ('MET', 'Metallica', 'tm', 'The Unforgiven'),
        ('STS', 'Swallow the Sun', 'doom', 'Falling World'),  # blackened death-doom with gothic edge
        ('FAE', 'Faetooth', 'doom', 'Strange Ways'),  # Fairy doom
        ('MDB', 'My Dying Bride', 'doom', 'Your Broken Shore'),
        ('FOE', 'Fall of Efrafa', 'crst', 'Pity the Weak'),
        ('LAC', 'Lacuna Coil', 'goth', 'Our Truth'),
        ('PRD', 'Paradise Lost', 'goth', 'Ghosts'),
        ('KTA', 'Katatonia', 'goth', 'For My Demons'),
        ('CAT', 'Cattle Decapitation', 'gcr', 'Manufactured Extinct'),
        ('RAM', 'Rammstein', 'im', 'Feuer Frei!'),
        ('RNC', 'Raunchy', 'im', 'A Heavy Burden'),
        ('ELV', 'Eluveitie', 'celt', 'Quoth the Raven'),
        ('GRA', 'Grai', 'fm', 'Song of Dead Water'),
        ('KPK', 'Korpiklaani', 'fm', 'Ruumiinmultaa'),
        ('ALE', 'Alestorm', 'pirt', 'Keelhauled'),
        ('NWS', 'Nightwish', 'sm', 'Ghost Love Score'),
        ('AVT', 'Avantasia', 'sm', 'The Scarecrow'),  # Metal opera
        ('LOG', 'Lamb of God', 'gm', 'Memento Mori'),
        ('GOJ', 'Gojira', 'pgm', 'The Axe'),  # Prog/Groove/Death
        ('JIN', 'Jinjer', 'pgm', 'On The Top'),
        ('TOO', 'Tool', 'prg', 'Lateralus'),
        ('DFT', 'Deftones', 'alt', 'Digital Bath'),
        ('SLT', 'Sleep Token', 'alt', 'Alkaline'),
        ('ZAA', 'Zeal and Ardor', 'alt', 'Gotterdamerung'),
        ('NOK', 'Knocked Loose', 'hcp', 'Deep in the Willow'),
        
    )
]
elements = genre_nodes + genre_edges + band_nodes + microgenre_nodes# + band_edges
app.layout = html.Div([
    dcc.Location(id="location"),
    cyto.Cytoscape(
        id='cytoscape',
        # layout = {'name': 'grid'},
        layout={'name': 'fcose', 'nodeSeparation': 100, 
                'idealEdgeLength': 250, 'nodeDimensionsIncludeLabels': True,
                'uniformNodeDimensions': False}, 
        # layout={'name': 'cose-bilkent', 'idealEdgeLength': 200},
        style={'width': '100%', 'height': '550px'},
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

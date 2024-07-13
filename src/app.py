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
            'source-arrow-color': 'slategrey',
            'source-arrow-shape': 'triangle',
            'arrow-scale': 2
        }
    },
    {
        'selector': '.genre_node',
        'style': {
            'background-color': 'red',
            'background-opacity': '0.2',
            'font-weight': 'bold',
            'shape': 'roundrectangle',
            'width': '100%',
            'height': '100%'
        }
    },
    {
        'selector': '.band_node',
        'style': {
            # 'background-color': 'slategrey',
            'background-fit': 'cover',
            'background-image': 'data(url)',
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
        ('sldg', 'Sludge Metal'),
              
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
        ('djnt','"Djent"', 'prg'),
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
        ('doom', 'sldg'),
        ('tm', 'gcr'),
        
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
        'data': {'id': id, 'label': name, 'parent': parent, 'song': song,
                 'url': f"https://flagcdn.com/w2560/{country}.png"},
        'classes': 'band_node'
    }
    for id, name, parent, song, country in (
        ('INF', 'In Flames', 'mdm', 'Delight and Angers','se'),
        ('INS', 'Insomnium', 'mdm', 'Down With The Sun', 'fi'),
        ('ALC', 'Alcest', 'bg', 'Kodama', 'fr'),
        ('ULV', 'Ulver', 'bm', 'I Troldskog Faren Vild', 'no'),
        ('HFS', 'Harakiri for the Sky', 'bg', 'Manifesto', 'au'),
        ('KAK', 'Kekht Arakh', 'abm', 'Swordsman', 'fi'),
        ('ELL', 'Ellende', 'abm', 'Wind', 'de'),
        ('MGL', 'MGLA', 'bm', 'Exercises in Futility V', 'pl'),
        ('MUL', 'My Useless Life', 'dsbm', 'A Desolate Heart', 'us'),
        ('WHW', 'White Ward', 'bjaz', 'Cronus', 'ua'),
        ('SVB', 'Svalbard', 'bg', 'Listen to Someone', 'ca'),  # Try not to die until you're dead
        ('ELD', 'Elderwind', 'abm', 'The Magic Of Nature', 'ru'), # Maybe remove
        ('COF', 'Cult of Fire', 'abm', 'Kali Ma', 'cz'), # Maybe remove
        ('BSB', 'Black Sabbath', 'hm', 'Heaven and Hell', 'gb'),
        ('IRN', 'Iron Maiden', 'hm', 'The Trooper', 'gb'),
        ('ICE', 'Iced Earth', 'hm', 'Anthem', 'us'),
        ('DTH', 'Death', 'dm', 'Spirit Crusher', 'us'),
        ('SEP', 'Septicflesh', 'dm', 'Anubis', 'gr'),
        ('RVC', 'Revocation', 'dm', 'The Grip Tightens', 'us'),
        ('AMA', 'Amon Amarth', 'vm', 'Twilight Of The Thunder God', 'no'),  # Cry of the Blackbirds
        ('BLK', 'Be\'lakor', 'pmdm', 'Abeyance', 'au'),  # Root to Sever, Smoke of many fires
        ('SWK', 'Soilwork', 'mdm', 'Distortion Sleep', 'se'),
        ('DTQ', 'Dark Tranquility', 'mdm', 'Time out of Place', 'se'),
        ('OBC', 'Orbit Culture', 'mdm', 'See Through Me', 'se'),
        ('HNT', 'The Haunted', 'mdm', 'The Fallout', 'se'),
        ('DIS', 'Disarmonia Mundi', 'mdm', 'Celestial Furnace', 'it'),
        ('UTA', 'Unleash the Archers', 'pm', 'Apex', 'ca'),
        ('TRI', 'Triosphere', 'pm', 'Steal Away the Light', 'no'),
        ('ODO', 'Orden Ogan', 'pm', 'Gunman', 'de'),
        ('PWF', 'Powerwolf', 'pm', 'Army of the Night', 'de'),
        ('OPT', 'Opeth', 'prg', 'Reverie / Harlequin Forest', 'se'),
        ('CAL', 'Caligulas Horse', 'prg', 'The World Breathes With me', 'au'),
        ('DRT', 'Dream Theater', 'prg', 'Pull Me Under', 'us'),
        ('TVM', 'Trivium', 'mcr', 'The Sin and the Sentence', 'us'),
        ('ALD', 'As I Lay Dying', 'mcr', 'Through Struggle', 'us'),
        ('LMK', 'Landmvrks', 'mcr', 'Creature', 'fr'),
        ('AVA', 'Aviana', 'dcr', 'Oblivion', 'se'),
        ('ALT', 'Allt', 'pmcr', 'Remnant', 'se'),
        ('ARC', 'Architects', 'mcr', 'Dead Man Talking', 'gb'),
        ('PWD', 'Parkway Drive', 'mcr', 'Carrion', 'au'),
        ('THN', 'Thornhill', 'mcr', 'Human', 'au'),
        ('BRT', 'Bury Tomorow', 'mcr', 'The Agonist', 'gb'),
        ('CRY', 'Crystal Lake', 'mcr', 'Curse', 'jp'),
        ('MNM', 'Monuments', 'djnt', 'False Providence', 'gb'),
        ('ERA', 'ERRA', 'pmcr', 'Nigh to Silence', 'us'),
        ('NRT', 'Northlane', 'pmcr', '4D', 'au'),
        ('SPB', 'Spiritbox', 'pmcr', 'The Beauty of Suffering', 'ca'),
        ('INA', 'Invent Animate', 'pmcr', 'Purity Weeps', 'us'),
        ('SIP', 'Silent Planet', 'pmcr', 'Second Sun', 'us'),
        ('CUR', 'Currents', 'pmcr', 'The Place Where I Feel Safest', 'us'),
        ('ECB', 'Electric Callboy', 'ecr', 'Hypa Hypa', 'de'),
        ('ESH', 'Enter Shikari', 'ecr', '...Meltdown', 'gb'),
        ('CRS', 'Crossfaith', 'ecr', 'ZERO', 'jp'),
        ('BSC', 'Blood Stain Child', 'ecr', 'Eternal', 'jp'),
        ('NOO', 'Noosphera', 'ecr', 'Reflejos', 'mx'),
        ('SLP', 'Slipknot', 'num', 'Wait and Bleed', 'us'),
        ('MAC', 'Machine Head', 'num', 'Circle the Drain', 'us'),
        ('LIP', 'Linkin Park', 'num', 'Don\'t Stay', 'us'),
        ('BLW', 'Bloodywood', 'num', 'Machi Bhasad', 'in'),
        ('SOD', 'System of a Down', 'num', 'B.Y.O.B', 'am'),
        ('WIT', 'Within Temptation', 'pop', 'Bleed Out', 'nl'),
        ('BCH', 'Blind Channel', 'pop', 'Flatline', 'fi'),
        ('BAD', 'Bad Omens', 'pop', 'Artificial Suicide', 'us'),
        ('BMT', 'Bring Me The Horizon', 'pop', 'Doomed', 'gb'),
        ('FFA', 'Fit for an Autopsy', 'dcr', 'Two Towers', 'us'),
        ('WCH', 'Whitechapel', 'dcr', 'A Bloodsoaked Symphony', 'us'),
        ('SOI', 'Shadow of Intent', 'pdcr', 'Intensified Genocide', 'us'),
        ('DWP', 'The Devil Wears Prada', 'pop', 'Broken', 'us'),
        ('ALP', 'Alpha Wolf', 'mcr', 'Bleed 4 U', 'au'),
        ('VOV', 'Void of Vision', 'mcr', 'Empty', 'au'),
        ('FUT', 'Future Palace', 'mcr', 'Malphas', 'de'),
        ('BOU', 'Boundaries', 'mcr', 'Inhale the Grief', 'us'),
        ('HLB', 'Humanity\'s Last Breath', 'pdcr', 'Instill', 'se'), # Blackened Deathcore with Thall
        ('VLJ', 'Vildjharta', 'thl', 'lavender haze', 'se'),
        ('MIR', 'Mirar', 'thl', 'Franka', 'fr'),
        ('MGD', 'Megadeth', 'tm', 'The Scorpion', 'us'),
        ('MCH', 'Melechech', 'tm', 'Multiple Truths', 'il'),  # blackened thrash metal
        ('MET', 'Metallica', 'tm', 'The Unforgiven', 'us'),
        ('STS', 'Swallow the Sun', 'doom', 'Falling World', 'fi'),  # blackened death-doom with gothic edge
        ('FAE', 'Faetooth', 'doom', 'Strange Ways', 'us'),  # Fairy doom
        ('MDB', 'My Dying Bride', 'doom', 'Your Broken Shore', 'gb'),
        ('FOE', 'Fall of Efrafa', 'crst', 'Pity the Weak', 'gb'),
        ('MAR', 'Marno', 'crst', 'Samota', 'cz'),
        ('LAC', 'Lacuna Coil', 'goth', 'Our Truth', 'it'),
        ('PRD', 'Paradise Lost', 'goth', 'Ghosts', 'gb'),
        ('KTA', 'Katatonia', 'goth', 'For My Demons', 'se'),
        ('CAT', 'Cattle Decapitation', 'gcr', 'Manufactured Extinct', 'us'),
        ('RAM', 'Rammstein', 'im', 'Feuer Frei!', 'de'),
        ('RNC', 'Raunchy', 'im', 'A Heavy Burden','dk'),
        ('ELV', 'Eluveitie', 'celt', 'Quoth the Raven', 'ch'),
        ('GRA', 'Grai', 'fm', 'Song of Dead Water', 'ru'),
        ('KPK', 'Korpiklaani', 'fm', 'Ruumiinmultaa', 'fi'),
        ('TEN', 'Tengger Cavalry', 'fm', 'Ride Into Grave and Glory', 'cn'),
        ('ALE', 'Alestorm', 'pirt', 'Keelhauled', 'gb'),
        ('NWS', 'Nightwish', 'sm', 'Ghost Love Score', 'fi'),
        ('AVT', 'Avantasia', 'sm', 'The Scarecrow', 'de'),  # Metal opera
        ('LOG', 'Lamb of God', 'gm', 'Memento Mori', 'us'),
        ('AWE', 'Alien Weaponry', 'gm', 'Ahi Ka', 'nz'),
        ('SPL', 'Sepultura', 'gm', 'Roots Bloody Roots', 'br'),
        ('GOJ', 'Gojira', 'pgm', 'The Axe', 'fr'),  # Prog/Groove/Death
        ('JIN', 'Jinjer', 'pgm', 'On The Top', 'ua'),
        ('TOO', 'Tool', 'prg', 'Lateralus', 'us'),
        ('DFT', 'Deftones', 'alt', 'Digital Bath', 'us'),
        ('LOA', 'Loathe', 'alt', 'Screaming', 'gb'),
        ('SLT', 'Sleep Token', 'alt', 'Alkaline', 'gb'),
        ('ZAA', 'Zeal and Ardor', 'alt', 'Gotterdamerung', 'ch'),
        ('NOK', 'Knocked Loose', 'hcp', 'Deep in the Willow', 'us'),
        ('BWA', 'Beastwars', 'sldg', 'Damn the Sky', 'nz'),
        ('MAS', 'Mastodon', 'sldg', 'The Motherload', 'us'),
        ('MES', 'Meshuggah', 'djnt', 'Bleed', 'se'),
        
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
    # app.run_server(host="0.0.0.0", port="8050")
    app.run(debug=True)

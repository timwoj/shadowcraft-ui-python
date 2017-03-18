from flask import Flask, render_template, url_for, redirect, json, jsonify, request
from flask_pymongo import PyMongo
from werkzeug.routing import BaseConverter
from bson import json_util

import shadowcraft_ui
from shadowcraft_ui import backend

app = Flask('shadowcraft_ui')
app.config['SECRET_KEY'] = 'shhhhhhhh!'
app.config['MONGO_DBNAME'] = 'roguesim_python'

# Have to do this so that the request object sent to the /engine endpoint doesn't
# overrun the limit
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

mongo = PyMongo(app)


class RegexConverter(BaseConverter):

    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]
app.url_map.converters['regex'] = RegexConverter


@app.route('/')
def main():
    return render_template('index.html')

# Main route for the application. Loads a character.


@app.route('/<regex("(us|eu|kr|tw|cn|sea)"):region>/<realm>/<name>')
def character_show(region, realm, name):
    data = shadowcraft_ui.get_character_data(mongo, region, realm, name)
    character_json = json.dumps(data, indent=4, default=json_util.default)
    return render_template('index.html', character_json=character_json)

# Refreshes a character from the armory and redirects to the main route.
# TODO: Flask adds a "redirecting" page before redirecting. Is there a way
# to keep it from doing that?


@app.route('/<regex("(us|eu|kr|tw|cn|sea)"):region>/<realm>/<name>/refresh')
def character_refresh(region, realm, name):
    shadowcraft_ui.refresh_character(mongo, region, realm, name)
    url = url_for('character_show', region=region, realm=realm, name=name)
    return redirect(url)

# Requests a character page based on a saved sha value.


@app.route('/<regex("(us|eu|kr|tw|cn|sea)"):region>/<realm>/<name>/#!/<sha>')
def character_sha(region, realm, name, sha):
    shadowcraft_ui.get_character_data(mongo, region, realm, name, sha=sha)
    url = url_for('character_show', region=region, realm=realm, name=name)
    return redirect(url)

# TODO: are these really necessary? Can't we just return 400/500 errors when
# necessary and configure flask to handle them as such?


@app.route('/error')
def error():
    return render_template('500.html')


@app.route('/missing')
def missing():
    return render_template('404.html')


@app.route('/engine', methods=['POST'])
def engine():
    print(request.get_json())
    dummy_data = {
        "breakdown": {
            "poison_bomb": 22362.651670700066,
            "mutilate": 77130.871980695,
            "envenom": 79767.73105787819,
            "garrote_ticks": 28991.377393848437,
            "t19_2pc": 19898.91495707033,
            "Mark of the Hidden Satyr": 10597.53742844213,
            "fan_of_knives": 9581.165833697387,
            "kingsbane_ticks": 7364.104322627836,
            "rupture_ticks": 115349.40396136601,
            "Recursive Strikes": 18139.76717988857,
            "Fel-Crazed Rage": 39478.02919162352,
            "from_the_shadows": 14713.38371860071,
            "kingsbane": 5816.887059079585,
            "autoattack": 28360.370985372523
        },
        "oh_speed_ep": {
            "oh_2.6": 722.0948164256916,
            "oh_1.8": 0.0,
            "oh_2.4": 541.5711123192618,
            "oh_1.7": -90.26185205321491
        },
        "total_dps": 477552.1967408903,
        "oh_ep": {
            "oh_mark_of_the_thunderlord": 214.98855692798185,
            "oh_mark_of_the_frostwolf": 178.32943964918255,
            "oh_dancing_steel": 46.24682371992041,
            "oh_mark_of_the_bleeding_hollow": 168.3405467303374,
            "oh_mark_of_the_shattered_hand": 16.27133904916045,
            "oh_mark_of_warsong": 87.06496095559233,
            "oh_dps": 0.3186876111711379
        },
        "mh_ep": {
            "mh_mark_of_the_thunderlord": 214.98855692798185,
            "mh_mark_of_warsong": 87.06496095559233,
            "mh_mark_of_the_shattered_hand": 16.27133904916045,
            "mh_dps": 0.6373752223422758,
            "mh_mark_of_the_bleeding_hollow": 168.3405467303374,
            "mh_mark_of_the_frostwolf": 178.32943964918255,
            "mh_dancing_steel": 46.24682371992041
        },
        "other_ep": {
            "duskwalkers_footpads": "not allowed",
            "rogue_t18_4pc_lfr": 0.0,
            "mark_of_the_claw": 412.93223164878185,
            "insignia_of_ravenholdt": 1620.2303916086396,
            "mantle_of_the_master_assassin": 0.0,
            "journey_through_time_2pc": 0.0,
            "greenskins_waterlogged_wristcuffs": 0.0,
            "rogue_t18_4pc": 0.0,
            "shivarran_symmetry": 0.0,
            "mark_of_the_distant_army": 659.6905556061445,
            "rogue_t18_2pc": 0.0,
            "thraxis_tricksy_treads": 0.0,
            "denial_of_the_half_giants": 0.0,
            "rogue_t19_2pc": 1885.8573125801706,
            "rogue_orderhall_8pc": 328.19592530515627,
            "the_dreadlords_deceit": 587.4933742309903,
            "march_of_the_legion_2pc": 911.1949867527755,
            "jacins_ruse_2pc": 607.3819125892312,
            "cinidaria_the_symbiote": 1357.755391646429,
            "mark_of_the_hidden_satyr": 1004.3484028091957,
            "zoldyck_family_training_shackles": 1187.1210698056998,
            "rogue_t19_4pc": 1259.9561269878698,
            "shadow_satyrs_walk": 0.0,
            "kara_empowered_2pc": 0.0
        },
        "ep": {
            "agi": 1.0,
            "mastery": 0.8068330786600924,
            "ap": 1.0,
            "haste": 0.4640613772017242,
            "crit": 0.9667989720771437,
            "versatility": 0.8797969179846511
        },
        "mh_speed_ep": {
            "mh_1.7": 169.87911163021425,
            "mh_2.4": -506.63565423828584,
            "mh_2.6": -544.6375544129845,
            "mh_1.8": 0.0
        },
        "proc_ep": {
            "tempered_egg_of_serpentrix": {
                "900": 1006.9380747694728,
                "905": 1055.0328509716737,
                "910": 1105.2908549389792,
                "915": 1158.2454852983988,
                "920": 1213.155910623522,
                "925": 1271.2370944536647,
                "930": 1331.7778386194739,
                "935": 1395.2226419767867,
                "940": 1461.8382038391082,
                "945": 1531.3874581499908,
                "820": 474.1913794132232,
                "950": 1604.6112363358445,
                "825": 500.53534493618065,
                "830": 524.4493833805288,
                "835": 549.6080186212389,
                "840": 575.7149180877382,
                "845": 603.036781093553,
                "850": 631.840306952177,
                "855": 662.0958624065421,
                "860": 693.5960146572799,
                "865": 726.5185632467123,
                "870": 761.426540058906,
                "875": 797.5494804104042,
                "880": 835.8652817840643,
                "885": 875.3960466970291,
                "890": 917.3863719456605,
                "895": 961.065792846491
            },
            "faulty_countermeasure": {

            },
            "darkmoon_deck_dominion": {
                "900": 1937.9315673979734,
                "905": 2030.1384569627576,
                "910": 2126.454774247831,
                "915": 2227.7042074995074,
                "920": 2332.220600084457,
                "925": 2443.313964583502,
                "930": 2559.3164539359655,
                "935": 2680.2192316024984,
                "940": 2807.6677043167406,
                "815": 864.2169213993243,
                "945": 2939.995377048711,
                "820": 914.3137563843167,
                "950": 3079.6706445281684,
                "825": 965.2340060419934,
                "830": 1011.1357002509792,
                "835": 1059.5308063507289,
                "840": 1109.5835245695844,
                "845": 1162.1265924883598,
                "850": 1217.991866570346,
                "855": 1276.3432499689316,
                "860": 1336.3454180089452,
                "865": 1399.6629280223374,
                "870": 1467.125503426636,
                "875": 1536.2317235194218,
                "880": 1609.4764376077958,
                "885": 1685.1914647840506,
                "890": 1765.8687114532754,
                "895": 1849.8398375553668
            },
            "windscar_whetstone": {
                "900": 652.142586875286,
                "905": 683.27906784005,
                "910": 715.8389760877845,
                "915": 750.1371189253259,
                "920": 785.7001529920384,
                "925": 823.3173613557484,
                "930": 862.5154006558416,
                "935": 903.6102105995197,
                "940": 946.7591948401846,
                "945": 991.806082124821,
                "820": 307.10471940218724,
                "950": 1039.2230834136456,
                "825": 324.1745227940636,
                "830": 339.66349524954586,
                "835": 355.94401557360646,
                "840": 372.85528291169413,
                "845": 390.5580981183386,
                "850": 409.2087324465982,
                "855": 428.80831829683825,
                "860": 449.19718721488323,
                "865": 470.5350076549085,
                "870": 493.13658692373974,
                "875": 516.5297140611493,
                "880": 541.3440036807668,
                "885": 566.9498411689518,
                "890": 594.1353771931443,
                "895": 622.4272683927298
            },
            "ravaged_seed_pod": {
                "865": 65.51648499090845,
                "930": 120.09639127940316,
                "900": 90.80483161383549,
                "870": 68.6659007290161,
                "935": 125.82048760512073,
                "905": 95.14026150649032,
                "875": 71.92162585913564,
                "940": 131.8269682533439,
                "910": 99.67502150915799,
                "880": 75.37668109926803,
                "945": 138.09922238156975,
                "850": 56.97851194558933,
                "915": 104.44897764382807,
                "885": 78.94136789989341,
                "950": 144.70369335980976,
                "855": 59.7060122841954,
                "920": 109.4023308775162,
                "890": 82.72863999003997,
                "860": 62.546466351797214,
                "925": 114.6380684337099,
                "895": 86.66873183118268
            },
            "nightmare_egg_shell": {
                "900": 699.2274221898376,
                "905": 732.6078721230818,
                "910": 767.5383301134561,
                "915": 804.3631609707631,
                "920": 842.4803059635766,
                "925": 882.8364931159041,
                "930": 924.9157357824415,
                "935": 968.9764827464118,
                "940": 1015.2772540636458,
                "945": 1063.646306022192,
                "820": 329.20561184333985,
                "950": 1114.5143909598432,
                "825": 347.5223193047586,
                "830": 364.1194823551418,
                "835": 381.57694555976326,
                "840": 399.72276158576545,
                "845": 418.64297648297224,
                "850": 438.6816577248357,
                "855": 459.66687240815435,
                "860": 481.51268286300154,
                "865": 504.477187788711,
                "870": 528.6464918325468,
                "875": 553.7626525871532,
                "880": 580.3418650007477,
                "885": 607.8681426223656,
                "890": 637.0297720546542,
                "895": 667.3107631664441
            },
            "tirathons_betrayal": {

            },
            "horn_of_valor": {
                "900": 1232.3200195602255,
                "905": 1291.310091189346,
                "910": 1352.7891953766616,
                "915": 1417.504041889619,
                "920": 1484.7079209607662,
                "925": 1555.894252125034,
                "930": 1629.818519103289,
                "935": 1707.4763349188345,
                "940": 1789.1166028274897,
                "945": 1874.241516317616,
                "820": 580.4423925700803,
                "950": 1963.84668841249,
                "825": 612.5509125707426,
                "830": 641.9214967573852,
                "835": 672.5365972231281,
                "840": 704.6451172237904,
                "845": 737.9981535035587,
                "850": 773.3424158298627,
                "855": 810.4290009469105,
                "860": 848.7601023430426,
                "865": 889.0824297857267,
                "870": 931.8937897866117,
                "875": 976.1985693223999,
                "880": 1022.9923814163889,
                "885": 1071.2796130452919,
                "890": 1122.802586999842,
                "895": 1176.3167870009388
            },
            "infernal_alchemist_stone": {
                "835": 1036.2055418254124,
                "840": 1085.477202877691,
                "845": 1136.9998535211937,
                "815": 844.8714265716196,
                "850": 1191.273713665071,
                "820": 894.1430876239036,
                "855": 1248.2987833093337,
                "825": 943.6648586307658,
                "860": 1307.8249524994037,
                "830": 988.9347604097635
            },
            "spontaneous_appendages": {
                "865": 902.9074974016004,
                "930": 1655.0757848590965,
                "900": 1251.3870739674894,
                "870": 946.2839632201678,
                "935": 1733.9203000762825,
                "905": 1311.1495389592449,
                "875": 991.1582351788846,
                "940": 1816.7190235034375,
                "910": 1373.608055003243,
                "880": 1038.7884704354556,
                "945": 1903.1723939125493,
                "850": 785.2398470318843,
                "915": 1439.4216568011743,
                "885": 1087.9165118321755,
                "950": 1994.149138864898,
                "855": 822.8347811494991,
                "920": 1507.6617045461253,
                "890": 1140.0701216319944,
                "860": 861.9574775300633,
                "925": 1579.8559605010669,
                "895": 1194.3805722736097
            },
            "arcanogolem_digit": {
                "865": 899.044380504477,
                "930": 1647.9717680556191,
                "900": 1246.0305442844822,
                "870": 942.2263920674925,
                "935": 1726.4941758929108,
                "905": 1305.5120651333557,
                "875": 986.9172239164292,
                "940": 1808.9480168695356,
                "910": 1367.7349636847894,
                "880": 1034.3281824779876,
                "945": 1895.014526136379,
                "915": 1433.2730166672422,
                "885": 1083.2479613254675,
                "950": 1985.607496260964,
                "920": 1501.2124315132019,
                "890": 1135.1853807447678,
                "860": 858.2637308049464,
                "925": 1573.083279498495,
                "895": 1189.247899158314
            },
            "chrono_shard": {
                "900": 408.89713571001954,
                "905": 416.6688559634844,
                "910": 424.50383197226415,
                "915": 432.5916240183837,
                "920": 440.6163054272361,
                "925": 449.02018604912496,
                "930": 457.48733700734385,
                "935": 466.0809488849049,
                "940": 474.9274041380377,
                "945": 483.83714081370965,
                "820": 300.92168369142223,
                "950": 492.99973283779013,
                "825": 308.88196617821836,
                "830": 314.7574594732166,
                "835": 320.7593484413357,
                "840": 326.76127885045474,
                "845": 332.8264295991787,
                "850": 339.1443400206187,
                "855": 345.58865604848035,
                "860": 352.0962002520323,
                "865": 358.6669740882789,
                "870": 365.55370403332097,
                "875": 372.37730703383,
                "880": 379.51687523298756,
                "885": 386.5301368363814,
                "890": 393.92255533783595,
                "895": 401.3150371871465
            },
            "memento_of_angerboda": {
                "900": 746.3707336969934,
                "905": 760.5125773861519,
                "910": 775.0747579620087,
                "915": 789.6414032772562,
                "920": 804.628897067083,
                "925": 820.0376337711322,
                "930": 835.4513623434685,
                "935": 851.7036702062144,
                "940": 867.9615259771282,
                "945": 884.2249305760774,
                "820": 547.9986293467562,
                "950": 901.328339889645,
                "825": 562.4955732904348,
                "830": 573.2676155383733,
                "835": 584.4565694767899,
                "840": 595.2336239850583,
                "845": 606.4277835527819,
                "850": 618.039343178319,
                "855": 630.0686088456641,
                "860": 641.6859763774643,
                "865": 654.1363224235306,
                "870": 666.589944618847,
                "875": 679.046843383014,
                "880": 692.3378140444297,
                "885": 705.2169978853558,
                "890": 718.5153104881556,
                "895": 732.2331020257086
            },
            "giant_ornamental_pearl": {
                "900": 765.2947356881,
                "905": 801.8352670209413,
                "910": 840.0435269408428,
                "915": 880.291598319819,
                "920": 922.0246790183508,
                "925": 966.169654047972,
                "930": 1012.1683991006606,
                "935": 1060.3963192169342,
                "940": 1111.0328114957888,
                "945": 1163.8918345012337,
                "820": 360.3888388932321,
                "950": 1219.5381568782743,
                "825": 380.42151494896524,
                "830": 398.5970988131336,
                "835": 417.7028898573384,
                "840": 437.5495244770642,
                "845": 458.32304410832916,
                "850": 480.2094901871298,
                "855": 503.20886271347683,
                "860": 527.1384424198549,
                "865": 552.1776264052713,
                "870": 578.7018197102487,
                "875": 606.1528980267544,
                "880": 635.2717049303258,
                "885": 665.3207190139282,
                "890": 697.223503120598,
                "895": 730.4252551108162
            },
            "natures_call": {
                "865": 613.3681530837383,
                "930": 783.5861873456805,
                "900": 699.700144426762,
                "870": 625.0429692817183,
                "935": 798.5581911469134,
                "905": 713.3459090203734,
                "875": 636.7206688344795,
                "940": 813.5349110365999,
                "910": 726.995601743873,
                "880": 649.0502579405126,
                "945": 829.167821558458,
                "850": 579.6570997378451,
                "915": 740.6492231473088,
                "885": 661.3830604671791,
                "950": 844.8058687847204,
                "855": 590.6753743305384,
                "920": 754.9572313518762,
                "890": 674.3684298743101,
                "860": 602.3445849979615,
                "925": 769.2695525406579,
                "895": 686.707829646741
            },
            "kiljaedens_burning_wish": {
                "910": 1686.6431802230295
            },
            "nightblooming_frond": {
                "865": 1763.8815040555012,
                "930": 3233.4566820500913,
                "900": 2444.7269079343164,
                "870": 1848.5679397596368,
                "935": 3387.4574281655323,
                "905": 2561.5550601598256,
                "875": 1936.3288005223449,
                "940": 3549.283983520967,
                "910": 2683.414089753903,
                "880": 2029.4000318407575,
                "945": 3718.097868554966,
                "915": 2812.2604490265344,
                "885": 2125.266195030585,
                "950": 3895.8555355775143,
                "920": 2945.5786992934513,
                "890": 2227.281208337558,
                "860": 1683.9464525327871,
                "925": 3086.4432656132044,
                "895": 2333.4886194516585
            },
            "spiked_counterweight": {
                "900": 2288.8946054525422,
                "905": 2398.1797815126474,
                "910": 2512.4587600436826,
                "915": 2632.8389137921663,
                "920": 2757.658003070361,
                "925": 2889.6880014484314,
                "930": 3027.266669238651,
                "935": 3171.5013791875276,
                "940": 3322.94699823627,
                "945": 3481.0510205795995,
                "820": 1077.877436596022,
                "950": 3647.4756859052222,
                "825": 1137.7912605676142,
                "830": 1192.1564151270572,
                "835": 1249.2959043925748,
                "840": 1308.6525002870387,
                "845": 1370.785792023486,
                "850": 1436.2459242713076,
                "855": 1505.0352581664229,
                "860": 1576.596565631682,
                "865": 1651.487074744235,
                "870": 1730.8165193864988,
                "875": 1812.9202987348478,
                "880": 1900.0155194181962,
                "885": 1989.8850748076297,
                "890": 2085.300938473282,
                "895": 2184.6008707274473
            },
            "draught_of_souls": {
                "865": 2333.668230752214,
                "930": 4986.674447538883,
                "900": 3562.8231271586187,
                "870": 2486.643992445961,
                "935": 5264.812196072969,
                "905": 3773.5659597017548,
                "875": 2644.9685569961316,
                "940": 5556.856832033759,
                "910": 3993.9366373864514,
                "880": 2812.9209666878687,
                "945": 5861.738594849972,
                "915": 4226.074681355286,
                "885": 2986.222179236029,
                "950": 6182.666766235457,
                "920": 4466.770809894397,
                "890": 3170.220997497042,
                "860": 2189.250553628748,
                "925": 4721.373825860216,
                "895": 3361.70813975705
            },
            "chaos_talisman": {
                "900": 1412.6481257123357,
                "905": 1482.1226236981943,
                "910": 1551.5971216840526,
                "915": 1621.0716196699057,
                "920": 1702.1252006533882,
                "925": 1783.1787816368924,
                "930": 1864.2323626203913,
                "935": 1956.865026601525,
                "940": 2049.497690582659,
                "945": 2153.7094375614383,
                "820": 671.5868138632441,
                "950": 2257.9211845402124,
                "825": 706.3240628561706,
                "830": 741.0613118490971,
                "835": 775.798560842029,
                "840": 810.5358098349501,
                "845": 845.2730588278766,
                "850": 891.5893908184436,
                "855": 926.3266398113755,
                "860": 972.6429718019315,
                "865": 1018.9593037925039,
                "870": 1065.275635783076,
                "875": 1123.1710507712833,
                "880": 1169.4873827618555,
                "885": 1227.3827977500682,
                "890": 1285.2782127382864,
                "895": 1354.752710724134
            },
            "tiny_oozeling_in_a_jar": {
                "900": 4188.026234902049,
                "905": 4387.983920302476,
                "910": 4597.080439587747,
                "915": 4817.351035763563,
                "920": 5045.732964500955,
                "925": 5287.304453493775,
                "930": 5539.032397874296,
                "935": 5802.942160827805,
                "940": 6080.051363857157,
                "945": 6369.332505639083,
                "820": 1972.2097514517634,
                "950": 6673.83845068214,
                "825": 2081.836238788249,
                "830": 2181.3062707370345,
                "835": 2285.8545303796645,
                "840": 2394.4633962132943,
                "845": 2508.1504897407794,
                "850": 2627.923552644541,
                "855": 2753.782584924589,
                "860": 2884.7198448984927,
                "865": 3021.752954069097,
                "870": 3166.9072756216897,
                "875": 3317.129945047724,
                "880": 3476.4914483586026,
                "885": 3640.9212995429116,
                "890": 3815.5076061149102,
                "895": 3997.197503566063
            },
            "terrorbound_nexus": {
                "900": 1621.3612784497175,
                "905": 1698.7743846120047,
                "910": 1779.7279056986968,
                "915": 1864.9996279417,
                "920": 1953.4164966961746,
                "925": 2046.9421034328168,
                "930": 2144.3948931108093,
                "935": 2246.5654025560298,
                "940": 2353.844649983407,
                "945": 2465.837366980019,
                "820": 763.5268176416034,
                "950": 2583.729358784655,
                "825": 805.965044556633,
                "830": 844.4760885303123,
                "835": 884.9507239746558,
                "840": 926.9979326747565,
                "845": 971.0087328455323,
                "850": 1017.3783928999169,
                "855": 1066.1069128379102,
                "860": 1116.7990242465783,
                "865": 1169.849995538866,
                "870": 1226.0418631446416,
                "875": 1284.2015724190865,
                "880": 1345.8974464199528,
                "885": 1409.5569118914939,
                "890": 1477.143560304407,
                "895": 1547.4843370138515
            },
            "mark_of_dargrul": {
                "900": 1033.9516111805178,
                "905": 1083.320117669081,
                "910": 1134.9436859438422,
                "915": 1189.319586039702,
                "920": 1245.7076951140198,
                "925": 1305.3454060443362,
                "930": 1367.4925959880109,
                "935": 1432.6465349799498,
                "940": 1501.0616402473077,
                "945": 1572.483494562924,
                "820": 486.9083151076451,
                "950": 1647.6637851888706,
                "825": 513.9690565419947,
                "830": 538.5318833824064,
                "835": 564.3436675197897,
                "840": 591.1499917269791,
                "845": 619.2168376505551,
                "850": 648.7870580982632,
                "855": 679.8606530700979,
                "860": 712.1947697583246,
                "865": 746.0206965512631,
                "870": 781.8588323226488,
                "875": 818.9459253910117,
                "880": 858.2880802455671,
                "885": 898.8791923970944,
                "890": 941.9797835619746,
                "895": 986.8381664781472
            },
            "bloodthirsty_instinct": {
                "865": 493.18536834861885,
                "930": 629.0793610086049,
                "900": 562.3444292221598,
                "870": 502.7409698052219,
                "935": 640.9043045815025,
                "905": 572.872648776037,
                "875": 511.97275421436774,
                "940": 653.0533922708203,
                "910": 583.7249504887708,
                "880": 521.8524939070047,
                "945": 665.3646469349026,
                "850": 466.30069006992807,
                "915": 594.901346969957,
                "885": 531.5703824820081,
                "950": 678.0000697226856,
                "855": 475.20817058310297,
                "920": 605.9159112614063,
                "890": 541.6123173051857,
                "860": 484.1157438391134,
                "925": 617.4165655395201,
                "895": 551.8163403676895
            },
            "entwined_elemental_foci": {
                "865": 676.3879127823914,
                "930": 864.1216982420154,
                "900": 771.8340225926119,
                "870": 689.2619251506803,
                "935": 880.8769855398228,
                "905": 786.6453648863118,
                "875": 702.139436526936,
                "940": 897.6381640510639,
                "910": 801.4613243330169,
                "880": 715.9747355489337,
                "945": 914.4052347815606,
                "915": 816.7600616629716,
                "885": 729.3367865282319,
                "950": 932.1368318404394,
                "920": 832.063720346077,
                "890": 743.1800222343386,
                "860": 663.9940222735975,
                "925": 848.3292508993183,
                "895": 757.504861019844
            },
            "convergence_of_fates": {
                "865": 1899.578142187049,
                "930": 1576.577630709464,
                "900": 1192.039454701713,
                "870": 1899.578142187049,
                "935": 1651.6940287275072,
                "905": 1248.954571661538,
                "875": 1899.578142187049,
                "940": 1730.5662466464523,
                "910": 1308.4698716296798,
                "880": 989.5140892761434,
                "945": 1812.9053752431535,
                "915": 1371.1631730524311,
                "885": 1036.317383425847,
                "950": 1899.578142187049,
                "920": 1436.167748260353,
                "890": 1086.0097698070142,
                "860": 1899.578142187049,
                "925": 1504.928143369177,
                "895": 1137.7245207502053
            }
        },
        "engine_info": {
            "shadowcraft_build": "0.02",
            "wow_build_target": "7.1.5"
        },
        "talent_ranking": {
            "100": {
                "venom_rush": 20965.29648980929,
                "death_from_above": 12797.496456855326,
                "marked_for_death": 5985.364097719488
            },
            "75": {
                "internal_bleeding": "not implemented",
                "thuggee": "not implemented",
                "prey_on_the_weak": "not implemented"
            },
            "45": {
                "vigor": 13380.953341401007,
                "deeper_strategem": 17179.25875801855,
                "anticipation": 8072.673966635077
            },
            "15": {
                "hemorrhage": 32958.15264656034,
                "master_poisoner": 23530.379951038747,
                "elaborate_planning": 33503.77777267614
            },
            "90": {
                "alacrity": 43437.994832580676,
                "agonizing_poison": 28624.46233146265,
                "exsanguinate": 50107.53065422934
            },
            "60": {
                "elusiveness": "not implemented",
                "cheat_death": "not implemented",
                "leeching_poison": "not implemented"
            },
            "30": {
                "shadow_focus": "not implemented",
                "subterfuge": "not implemented",
                "nightstalker": "not implemented"
            }
        },
        "trinket_map": {
            "128705": "darkmoon_deck_dominion",
            "140802": "nightblooming_frond",
            "144259": "kiljaedens_burning_wish",
            "140806": "convergence_of_fates",
            "139329": "bloodthirsty_instinct",
            "140808": "draught_of_souls",
            "141321": "shivarran_symmetry",
            "133642": "horn_of_valor",
            "136715": "spiked_counterweight",
            "137099": "greenskins_waterlogged_wristcuffs",
            "137357": "mark_of_dargrul",
            "137486": "windscar_whetstone",
            "137539": "faulty_countermeasure",
            "137419": "chrono_shard",
            "133664": "memento_of_angerboda",
            "133976": "cinidaria_the_symbiote",
            "137369": "giant_ornamental_pearl",
            "137373": "tempered_egg_of_serpentrix",
            "137439": "tiny_oozeling_in_a_jar",
            "137312": "nightmare_egg_shell",
            "137049": "insignia_of_ravenholdt",
            "127842": "infernal_alchemist_stone",
            "139334": "natures_call",
            "144236": "mantle_of_the_master_assassin",
            "137100": "denial_of_the_half_giants",
            "137031": "thraxis_tricksy_treads",
            "137098": "zoldyck_family_training_shackles",
            "137537": "tirathons_betrayal",
            "133597": "infallible_tracking_charm",
            "137032": "shadow_satyrs_walk",
            "137459": "chaos_talisman",
            "137030": "duskwalkers_footpads",
            "139320": "ravaged_seed_pod",
            "140794": "arcanogolem_digit",
            "140796": "entwined_elemental_foci",
            "139325": "spontaneous_appendages",
            "137406": "terrorbound_nexus",
            "137021": "the_dreadlords_deceit"
        },
        "artifact_ranking": {
            "214368": 12656.05916579545,
            "192384": 9390.73695324565,
            "192315": 2826.0981292367214,
            "192326": 1749.5990038542077,
            "192422": 0,
            "192424": 1693.8210990008083,
            "192329": 3492.258525241865,
            "192428": 14713.38371860073,
            "214928": 2200.701367469621,
            "192657": 22362.651670700056,
            "192323": 0,
            "192310": 2344.0393966002157,
            "192759": 9090.206897393102,
            "192376": 1492.531996937003,
            "192345": 0,
            "192923": 25283.988912231056,
            "192349": 3944.5767535433406,
            "192318": 746.2659984685015
        }
    }
    return jsonify(dummy_data)


@app.route('/settings')
def settings():
    settings_data = backend.get_settings()
    return jsonify(settings_data)

# Endpoint for requesting a new debug SHA based on from character data.


@app.route('/get_sha', methods=['POST'])
def get_sha():
    # TODO: this should probably validate the JSON
    return shadowcraft_ui.get_debug_sha(mongo, request.form['data'])

# Endpoint for requesting item data by slot. Also able to filter by ilvl.


@app.route('/get_items_by_slot')
def get_items_by_slot():
    # TODO: this should probably take some sort of key to make sure that we're
    # only returning data to our clients and not leaving this open to abuse by
    # other people.
    slot = request.form['slot']
    min_ilvl = request.form['min_ilvl']
    max_ilvl = request.form['max_ilvl']
    return shadowcraft_ui.get_items_by_slot(mongo, slot, min_ilvl, max_ilvl)

# TODO: we probably need other endpoints here for gems, relics, and other
# types of data. Theoretically the event above might be able to handle those
# if we add another argument. Basically I'm trying to get rid of items-rogue.js
# as much as possible. Anything that can be requested on-the-fly via an endpoint
# should be moved to one.

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

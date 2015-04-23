from __future__ import division,print_function
import sys
sys.dont_write_bytecode = True
from sklearn.tree import DecisionTreeClassifier
import math

MAXS = [103.03, 98.758, 117.847134, 133.952332, 122.62, 120.372886, 138.16822, 153.293464, 150.597276, 112.059681, 112.737084, 110.24, 104.33, 140.263482, 129.61, 115.184231, 142.02653, 144.934923, 137.863824, 103.38, 118.379491, 114.161933, 155.180355, 142.246039, 129.27, 146.051788, 154.306858, 156.503337, 110.680556, 121.413167, 129.248715, 133.749023, 155.169054, 141.714952, 141.196357, 158.018236, 157.285441, 165.677924, 117.513889, 144.037381, 127.410197, 148.028781, 140.044, 126.187717, 158.405572, 144.02889, 149.55721, 156.444282, 146.28677, 132.403103, 116.00078, 127.159505, 149.509711, 146.452474, 144.615153, 135.108181, 131.86556, 156.448947, 156.400581, 129.007378, 122.3, 103.337212, 131.206868, 154.545519, 141.765734, 137.275716, 156.634332, 143.590929, 130.76747, 124.439399, 126.52, 99.719686, 108.30344, 155.19298, 130.707465, 143.559896, 149.066623, 126.301107, 107.950087, 146.890625, 134.7, 133.550958, 101.031738, 153.052355, 129.498372, 121.005208, 128.422309, 122.787543, 118.366808, 156.919271, 147.651394, 152.13, 108.220432, 150.164822, 124.931532, 137.21875, 147.190104, 121.06, 120.69, 160.925347, 152.223117, 160.139115, 187.611699, 162.941876, 136.51, 162.67, 178.442749, 160.53125, 129.542348, 160.707567, 165.126139, 164.065972, 140.380251, 163.508925, 159.350694, 166.149306, 153.04, 173.167923, 143.749537, 170.616558, 174.54, 122.114176, 126.405338, 107.45982, 78.319931, 80.518251, 77.79, 104.03, 115.93, 132.06, 127.54, 84.58538, 111.505198, 102.540371, 89.041287, 87.230835, 103.85, 100.38, 122.28323, 126.58724, 117.078071, 84.219435, 94.957784, 90.73801, 115.97, 121.07, 104.26, 113.077691, 119.150879, 107.226942, 99.349609, 99.042, 121.155165, 120.4984, 140.739678, 132.985935, 136.253879, 112.94, 131.193088, 134.760742, 140.599935, 100.931458, 104.704698, 87.744, 115.376695, 142.997884, 127.17296, 127.095106, 133.669759, 133.209147, 105.329536, 70.22052, 97.162489, 101.685167, 115.613607, 125.897244, 122.634657, 109.454861, 99.659288, 99.435547, 126.371311, 111.700412, 109.012478, 113.24154, 120.972968, 136.21837, 149.978895, 128.900174, 100.811632, 127.117622, 134.258464, 117.93, 98.334744, 130.463623, 143.139947, 142.352186, 143.29, 143.01, 141.48, 143.75434, 137.551432, 107.827181, 130.130351, 132.665744, 126.347982, 143.204861, 154.519531, 148.013455, 137.041124, 143.439019, 152.056098, 125.57805, 135.017768, 126.896701, 108.392795, 93.10102, 82.989149, 82.384332, 115.86556, 111.06684, 103.753255, 116.22, 148.64, 147.21, 139.031969, 130.38, 118.107653, 159.856536, 152.183858, 129.59, 114.252299, 109.377401, 122.643148, 138.535926, 163.43, 173.042643, 184.175754, 144.08, 131.112144, 106.820535, 138.95578, 129.888977, 70.003073, 61.994798, 61.097109, 65.705219, 55.771657, 53.050466, 73.218285, 61.138, 72.19254, 67.344855, 64.128639, 79.00215, 73.401706, 68.030016, 71.872287, 73.006117, 56.829074, 66.572, 49.482096, 50.746, 71.744375, 76.168165, 76.255, 83.696777, 80.454074, 85.155382, 90.068034, 68.770291, 74.132053, 64.040961, 66.151845, 58.639, 75.968621, 78.239597, 81.44043, 73.176866, 62.252496, 66.812174, 62.9273, 63.465278, 61.00401, 50.882351, 72.875, 77.046, 76.360352, 84.939724, 86.951769, 62.34668, 68.986328, 72.736328, 79.508375, 73.286146, 87.865397, 77.134291, 70.856445, 75.602539, 73.416551, 70.491102, 52.903646, 72.553, 53.162089, 80.314914, 84.647298, 70.167562, 80.480794, 69.990696, 65.512804, 74.881185, 60.901, 65.613498, 67.425266, 59.319119, 79.395454, 55.007378, 71.788086, 72.01671, 69.560004, 109.881727, 92.405165, 87.048394, 53.815216, 55.180556, 64.366469, 58.596951, 70.174208, 68.402344, 78.96875, 73.926649, 86.455078, 59.181532, 57.67589, 64.548828, 58.610514, 58.010715, 62.438477, 61.831814, 66.412109, 87.931858, 77.504, 75.771918, 99.624699, 97.462455, 93.335, 77.89919, 78.403361, 77.971992, 79.673123, 97.558445, 91.421, 92.562297, 95.46561, 86.001112, 94.900513, 98.167779, 85.221592, 98.98877, 69.724, 93.11803, 79.669072, 95.44, 65.679, 280.68463, 281.589452, 295.343346, 280.703008, 275.143831, 283.892746, 293.13187, 280.25668, 289.580356, 283.102525, 280.833599, 265.36145, 279.867968, 279.895729, 279.269745, 282.004679, 292.074978, 270.323893, 293.160522, 276.604953, 266.620643, 280.150028, 282.012532, 271.096232, 292.904351, 291.449083, 262.943427, 283.396077, 273.631293, 260.685554, 273.543966, 279.648663, 275.412598, 281.881972, 291.056613, 266.619195, 264.432359, 256.030599, 266.306132, 266.501953, 275.495018, 274.746783, 283.125407, 281.260417, 285.582465, 282.71, 275.875814, 267.800551, 280.173069, 277.913357, 262.992908, 280.934781, 289.812147, 278.05481, 279.556749, 296.185221, 276.727431, 281.393446, 279.793349, 282.007107, 277.823956, 275.6765, 276.987047, 270.861328, 274.65804, 291.245117, 283.139757, 276.595269, 277.423177, 272.785156, 254.828606, 284.879639, 267.133898, 261.467665, 270.953668, 263.253255, 271.97619, 278.097439, 281.069661, 278.193359, 299.626502, 271.82666, 271.950901, 258.652534, 262.821216, 265.991428, 281.795681, 262.858507, 271.808377, 285.995226, 270.981705, 260.542101, 265.293783, 270.064453, 263.87717, 283.864149, 258.582357, 259.910807, 276.680773, 280.572483, 299.924438, 295.287899, 306.91111, 308.737393, 288.90068, 298.914405, 271.528758, 290.19, 281.462446, 293.028212, 286.96384, 293.428718, 317.347999, 267.841268, 299.932183, 298.851481, 298.49, 280.778766, 299.002005, 310.737844, 298.242163, 300.933164, 277.652069, 266.84, 263.63, 266.263523, 262.960173, 295.547139, 268.778917, 268.246711, 262.156847, 276.061052, 273.481784, 271.492703, 267.992947, 267.649848, 271.564345, 272.136895, 265.588406, 257.813748, 277.690321, 251.439073, 251.514567, 259.28087, 254.870443, 258.328179, 265.544651, 266.962185, 261.071642, 268.003879, 266.55, 272.017541, 258.236708, 258.985297, 257.305718, 258.071506, 260.244358, 259.611654, 257.713433, 268.323188, 255.731771, 273.62816, 273.569363, 264.482476, 268.649414, 255.756131, 254.895643, 260.83, 259.106011, 251.45128, 258.334852, 267.93752, 283.55, 282.684733, 301.244141, 257.73329, 273.070095, 257.683051, 272.984592, 252.677517, 258.875651, 252.051602, 284.706055, 283.392198, 284.985297, 285.777886, 300.314019, 267.830838, 275.213759, 269.752387, 250.96, 251.88, 277.544271, 281.821994, 286.12793, 285.586697, 280.903429, 279.739583, 258.375217, 267.473524, 257.79145, 272.091549, 257.07015, 265.343424, 283.099609, 265.245443, 291.9375, 263.931858, 262.310113, 277.91645, 274.600043, 280.643853, 280.524631, 257.128038, 274.31326, 266.783746, 271.12, 263.18, 268.155165, 269.276042, 286.116753, 284.64, 275.058517, 283.803159, 264.600739, 276.965936, 275.345893, 264.008816, 266.945855, 287.576518, 279.785563, 270.843269, 263.92372, 280.924282, 292.190891, 289.311605, 274.38, 274.399062, 289.8502, 272.369062, 265.85845, 277.969743, 253.62, 258.265515, 261.928955, 253.543084, 251.966363, 256.705017, 260.040805, 275.232853, 278.996874, 256.900716, 265.69, 279.90469, 261.286635, 271.869509, 264.876519, 258.856954, 266.242174, 262.789714, 276.656047, 266.703803, 251.48, 251.252075, 271.869493, 277.548503, 296.318902, 282.917752, 286.539931, 274.955322, 266.298692, 276.039334, 268.418026, 263.743273, 250.979004, 294.854384, 292.672092, 298.899197, 281.379123, 297.359592, 290.617839, 302.978299, 256.810299, 275.674805, 272.082248, 261.921061, 302.32487, 301.983615, 257.651801, 274.84337, 296.539497, 271.533312, 263.211175, 271.580919, 263.949002, 263.231554, 271.534288, 269.954644, 264.29, 255.380317, 257.545573, 267.592448, 267.251194, 267.48, 264.711819, 291.671414, 261.209201, 269.06, 268.981554, 262.522786, 258.543837, 252.27, 310.739963, 291.494792, 278.773112, 290.652696, 271.033637, 259.89388, 288.886068, 258.245334, 263.88, 254.85, 275.493178, 272.11952, 264.45, 263.722385, 277.176866, 265.081055, 289.885308, 282.373481, 275.804036, 286.613824, 259.01612, 268.493896, 260.419325, 257.36, 281.009332, 302.953776, 298.215061, 294.554688, 293.882378, 277.0523, 280.591435, 288.399161, 283.779983, 292.913259, 273.313426, 290.714322, 281.52927, 294.51255, 285.958889, 277.486233, 253.296278, 265.282199, 303.49, 293.572049, 281.226664, 276.614251, 261.124503, 265.31884, 298.12, 259.524429, 250.800284, 280.120075, 256.943995, 252.49, 260.709301, 263.047356, 257.81, 268.15, 265.858558, 268.638299, 262.234097, 290.686778, 272.373942, 260.63, 256.95, 273.521349, 264.118625, 263.147976, 268.296604, 267.612278, 276.489041, 274.730955, 278.608371, 289.520806, 280.584581, 276.792372, 272.660414, 275.264323, 271.04, 288.967882, 288.473307, 256.92904, 293.927246, 297.544488, 305.05835, 279.98725, 289.69656, 302.61263, 306.373806, 285.641981, 299.669488, 261.505032, 276.018229, 285.825846, 284.638753, 312.31958, 308.712375, 312.014648, 291.583116, 270.174696, 276.563151, 266.2, 254.200955, 265.683268, 288.562391, 293.981052, 306.072727, 278.946886, 267.603461, 262.168837, 276.217556, 266.536519, 267.4713, 283.515354, 289.66626, 289.90606, 286.710422, 289.792535, 283.720052, 276.294976, 276.281196, 281.028697, 287.886393, 288.629639, 282.773275, 283.328559, 288.083333, 287.490451, 285.412326, 291.918023, 287.386176, 281.62, 306.244704, 289.746636, 274.288194, 284.867839, 267.318359, 285.79758, 260.945638, 285.168566, 288.500488, 299.013143, 297.97998, 273.35498, 269.012478, 305.247613, 271.463976, 271.212348, 284.523655, 288.882378, 292.417535, 296.931715, 284.082162, 288.08809, 297.203672, 292.48637, 300.379544, 325.199903, 291.919122, 300.103021, 283.7382, 292.055637, 287.064697, 312.583554, 283.061659, 289.942627, 271.712429, 295.141529, 296.813473, 307.629714, 293.23, 280.91, 130.800055, 130.590535, 122.514628, 123.836987, 138.04, 126.663873, 123.5, 129.466668, 134.36, 153.349091, 137.593026, 119.518894, 130.298286, 128.872233, 130.72, 124.828668, 138.038601, 123.440348, 121.856066, 126.177246, 132.57031, 124.471232, 136.852729, 141.753608, 137.14369, 123.913194, 125.120633, 127.47602, 122.915256, 120.630968, 125.129476, 141.441915, 152.07, 150.247504, 163.287055, 127.241916, 150.8109, 144.931912, 137.341254, 125.628798, 129.604823, 128.627469, 147.532959, 144.973145, 177.057834, 130.679416, 151.290799, 141.280599, 138.006293, 140.745117, 135.371216, 135.141168, 142.945502, 156.796224, 152.854329, 138.023546, 146.864041, 131.740451, 139.681207, 130.387912, 126.350545, 131.111491, 140.454753, 157.103082, 174.847656, 143.250651, 128.530273, 126.955078, 133.978407, 133.710124, 137.886692, 118.714464, 153.15625, 152.621799, 161.617622, 144.542535, 131.566298, 121.634983, 137.58, 131.540148, 137.495144, 122.173882, 139.390815, 156.691298, 135.169271, 150.709418, 131.771918, 130.527778, 120.790582, 125.087674, 134.743368, 136.754449, 120.739855, 129.173665, 124.96799, 142.572266, 124.575955, 144.507378, 131.735677, 121.068251, 160.508607, 170.74, 153.86, 164.864187, 183.359152, 184.239905, 177.552544, 170.461582, 178.039625, 188.135417, 182.434923, 202.594347, 170.724386, 184.49646, 169.339979, 174.272081, 194.570992, 188.114734, 187.110017, 185.190514, 165.806899, 146.958595, 136.888192, 116.541667, 116.536458, 116.412706, 120.773451, 116.541619, 116.663347, 123.848609, 119.655396, 116.541667, 121.911947, 120.709717, 122.88, 117.130656, 118.981364, 117.149468, 117.856771, 117.96403, 117.361382, 116.563314, 116.49, 116.32666, 116.589925, 117.761285, 116.634983, 118.470052, 116.067193, 119.71, 116.558485, 121.936252, 126.135742, 117.463921, 116.519911, 120.221408, 125.542969, 121.530111, 116.116808, 117.322645, 116.591037, 119.783803, 118.097928, 121.382324, 128.697076, 130.519368, 145.733724, 126.358561, 123.464193, 124.085503, 135.08138, 125.748164, 117.559245, 129.313802, 139.913032, 147.076714, 134.371311, 135.417101, 126.529839, 116.368056, 116.541667, 116.399523, 116.897135, 116.54248, 130.268663, 142.680556, 127.012153, 132.32194, 124.861111, 116.972005, 126.564453, 116.373101, 116.64228, 116.522678, 116.172201, 116.07628, 123.552409, 121.156141, 116.329861, 116.541667, 116.639323, 117.523512, 124.089193, 129.579563, 124.807888, 116.265842, 122.202691, 125.61697, 132.187283, 121.381185, 116.983181, 116.542209, 116.425049, 120.727902, 128.65446, 124.129991, 123.894314, 123.151042, 128.287435, 142.273003, 116.235243, 181.130975, 147.871919, 148.203832, 140.405357, 164.606488, 169.721483, 160.696309, 146.625007, 154.831116, 171.826765, 181.460002, 169.262709, 141.088684, 153.401666, 154.504591, 154.165419, 169.285543, 163.534993, 163.098019, 180.600246, 193.055151]
MINS = [-101.232277, -109.938104, -122.710953, -130.233622, -121.622267, -113.427107, -115.792626, -113.502901, -106.471034, -115.991273, -99.444085, -128.047072, -147.236104, -133.907413, -121.652032, -127.740506, -103.34337, -116.052887, -107.943373, -129.533207, -128.732059, -118.13742, -158.332113, -152.375661, -154.294773, -151.230279, -138.39586, -153.12028, -112.836148, -111.038479, -111.931709, -128.499917, -161.056464, -165.820747, -154.974894, -159.193088, -124.974338, -162.255534, -117.386783, -114.67, -124.7774, -133.98607, -161.649767, -149.374891, -138.462735, -165.183919, -129.470323, -139.692871, -125.087172, -127.717339, -129.35013, -134.814846, -155.156901, -143.803874, -147.195955, -161.694499, -135.362278, -142.209093, -125.840115, -145.656087, -147.716521, -137.636044, -139.765171, -140.378805, -142.65332, -134.226942, -142.467556, -140.527371, -140.821398, -141.315104, -153.051195, -123.654424, -115.784214, -131.077828, -136.028592, -112.698883, -138.285509, -140.236165, -130.602214, -132.810113, -122.826484, -129.669569, -133.537923, -131.948242, -129.051948, -110.918172, -131.89586, -131.550618, -120.22, -112.261719, -162.769179, -133.569173, -126.369846, -129.415473, -129.774306, -100.721463, -123.517415, -146.658312, -119.309896, -108.606662, -167.487397, -164.935404, -156.077546, -153.34886, -190.391835, -175.054026, -189.395284, -150.133745, -184.329163, -171.010946, -168.899618, -156.482693, -165.353632, -153.512017, -155.079492, -169.065755, -162.791805, -172.644336, -176.748949, -146.308081, -179.423884, -114.164568, -101.899632, -91.553343, -80.637, -105.053434, -85.673963, -81.40927, -100.997525, -86.768066, -78.503, -84.600444, -109.42, -96.118264, -93.339, -99.804674, -112.538045, -120.87561, -120.96306, -115.221159, -115.775845, -103.209866, -101.262248, -99.397786, -99.369276, -100.14, -90.955322, -88.81349, -83.386176, -78.518338, -106.712131, -88.041402, -101.369792, -91.932617, -100.02, -96.976349, -101.254693, -127.282878, -98.989149, -69.403, -93.769206, -103.911051, -83.590583, -91.178, -78.453505, -99.36263, -89.261502, -99.568983, -97.307237, -85.959663, -84.98763, -101.991272, -92.256551, -79.514106, -97.21875, -116.079427, -128.236871, -81.114529, -76.900065, -104.304036, -119.624783, -95.063646, -74.218831, -84.244629, -102.575629, -101.835558, -109.801921, -127.621962, -111.820313, -113.277561, -125.132053, -83.141177, -85.715149, -97.55816, -109.807373, -113.567654, -97.301866, -127.111165, -113.236437, -109.561523, -114.272352, -106.36694, -96.818454, -118.698758, -128.455485, -129.025608, -115.909939, -124.407444, -122.167643, -97.911024, -86.449219, -105.16048, -78.051, -100.806559, -117.340115, -120.473796, -113.816732, -103.245497, -83.247613, -75.543511, -76.063151, -106.039341, -133.012966, -144.440911, -136.263163, -108.533219, -87.663395, -98.69439, -115.709846, -91.651363, -118.081387, -92.372776, -89.304911, -113.506801, -122.409451, -117.197211, -145.043633, -90.029, -99.550898, -121.98, -76.768745, -87.152434, -71.078, -58.014915, -58.858, -61.02909, -63.385159, -57.491889, -62.585491, -62.62335, -60.030986, -59.182488, -74.652817, -71.276352, -66.512875, -66.63328, -62.532477, -71.823134, -67.180474, -61.55, -60.022461, -57.711155, -69.353895, -87.840902, -99.172065, -80.278537, -75.442274, -71.80976, -59.033447, -65.383518, -59.510959, -78.920736, -56.872025, -90.223199, -72.978054, -73.110487, -79.879232, -61.618761, -65.490126, -70.361, -93.91276, -67.269368, -81.255, -58.736, -78.119303, -95.534722, -76.388184, -75.422933, -72.78342, -70.833605, -63.593316, -55.15625, -66.115401, -59.779175, -88.409288, -89.701443, -84.864746, -86.881185, -93.372613, -75.359, -75.264323, -88.519748, -59.088706, -109.187229, -63.778375, -74.788466, -104.261068, -87.690755, -112.733073, -104.328451, -60.926649, -87.525391, -63.943098, -90.978366, -54.596876, -75.943169, -85.954319, -95.612088, -100.852214, -66.500543, -67.055, -67.766, -77.882518, -66.741781, -58.138156, -59.11225, -102.857856, -80.342231, -61.723741, -70.877062, -81.336155, -71.894965, -72.240657, -64.790582, -69.198161, -90.502062, -63.482639, -73.757053, -58.375434, -73.689453, -78.751953, -75.216905, -105.895613, -112.98159, -94.292215, -86.944682, -82.003467, -104.741841, -102.672879, -110.052687, -103.739544, -99.747548, -94.3235, -102.015055, -115.6265, -109.72, -101.057312, -113.507189, -87.321553, -104.256251, -110.709749, -114.653947, -88.586448, -47.520243, -39.746518, -20.986891, -27.375356, -17.24568, -30.230248, -26.450714, -27.242338, -30.545329, -30.652479, -36.970408, -20.383898, -19.795112, -23.739807, -12.142687, -19.574449, -10.049655, -22.067, -24.644, -32.499647, -27.284142, -16.073174, -8.334507, -20.392134, -19.43457, -14.220269, -23.553277, -19.814779, -26.327, -24.381673, -7.779619, -10.169705, -26.327067, -40.746813, -17.881293, -38.0574, -26.514757, -32.360135, -16.13661, -7.612522, -32.682638, -11.612061, -14.639, -19.302979, -24.955132, -35.085341, -32.105, -20.303331, -32.325467, -33.409071, -21.922526, -26.697293, -1.428833, -20.374973, -35.716933, -44.404487, -39.818739, -38.005154, -27.032444, -4.690213, -29.944387, -9.205363, -23.395291, -27.995, -49.903225, -43.907037, -45.080295, -35.54541, -38.292426, -13.111, -15.75649, -18.409, -14.157172, -26.078837, -33.166992, -48.678928, -44.876628, -49.919786, -48.5523, -28.471897, -13.469, -27.761203, -38.556695, -35.9037, -37.413059, -23.350911, -32.858073, -45.09337, -39.322266, -45.840495, -37.581546, -32.582709, -43.716, -31.607205, -29.859592, -25.316949, -19.678819, -25.843533, -29.892578, -49.675998, -5.309547, 1.465012, -24.0816, -31.229, -11.539895, -6.6563, -27.517, -31.62321, -29.393412, -49.014, -50.687547, -44.643473, -29.179, -47.344, -62.999247, -54.579, -23.541005, -32.221, -40.234015, -57.882654, -40.911142, -4.408, -3.901525, -0.479238, -5.267964, 0.517053, -2.190201, -0.5, -0.473002, -1.923623, -0.479262, -0.500888, -1.659409, -1.260796, -5.888262, 1.2114, -8.810805, -0.5, -7.434869, 0.082099, -0.5, -0.5, -0.497837, 0.021121, -2.654392, -1.442234, -2.804999, -16.777018, -3.464308, -15.264513, -1.495039, -0.5, -27.768066, -0.000543, -0.543918, -5.773492, -7.261909, -22.743951, -14.248589, -4.527507, -6.951063, -0.5, -5.758721, -28.954631, -2.968411, -5.855469, 0.27799, -6.724772, -9.233181, -2.359009, -8.782498, -4.332859, -8.990628, -11.731486, -2.43457, -9.87698, 1.057997, -7.618978, -24.325304, -11.25, -3.266602, -2.945513, -31.113634, -43.966743, -5.487103, -3.636285, -0.63227, -2.295085, -0.50003, -9.294705, -4.193685, -8.127443, -24.548292, -24.989176, -27.983941, -31.568251, -22.656087, -0.49957, -21.955729, -12.979384, -11.036133, -18.247991, -25.922784, -15.738688, -21.829841, -36.886258, -27.186252, -2.859484, -8.905328, -11.723307, -22.374891, -8.95796, -18.848416, -14.272705, -19.542331, -13.817196, -7.367018, -2.49566, -0.48519, -6.158637, -28.208333, -5.72659, -21.460844, -21.869829, -31.30359, -8.773911, -17.175316, -21.277405, -21.398265, -45.62748, -7.688778, -3.879333, -19.834465, -60.875981, -37.24899, -26.794986, -28.283949, -35.435716, -25.254295, -18.301, -12.493, -39.350881, -28.768911, -20.82208, -25.304287, -34.944359, -11.972276, -11.767069, -30.964654, -7.85709, -0.428545, -3.62972, -22.383442, -6.897438, -11.806, -54.14289, -50.781311, -36.537381, -31.603034, -9.2881, -13.914768, -13.542535, -23.970141, -3.136336, -6.12345, -1.824181, -50.186171, -52.571072, -25.77358, -12.650852, -45.208171, -41.489855, -14.629893, -0.433243, 0.54343, -3.106398, -31.435, -44.812446, -14.968913, -40.796441, -32.505602, -5.748047, -24.277167, -6.8517, -11.564345, -4.254042, -23.232747, -34.670681, -53.624186, -52.796984, -19.129666, -9.206299, -40.585355, -20.975484, -12.189, -6.193793, -12.951443, -33.397027, -34.100966, -20.26728, -4.739855, -30.3935, -22.598, -26.757121, -19.089491, -22.631402, -20.706543, -14.902018, -28.475369, -7.57921, -2.940213, -0.663194, -26.139, -22.222195, 2.070747, -22.548503, -17.458767, -18.341797, -39.051, -14.060167, -6.841526, -3.911024, -15.964115, -16.543, -17.330119, -17.494303, -25.127713, -27.030273, -17.147244, -27.906141, -13.56288, -8.964518, -8.890404, -14.503866, -39.492, -18.834527, -30.626899, -21.097114, -17.676432, -23.931, -21.897352, -12.103841, -10.856841, -45.487431, -52.949297, -26.892134, -17.539, -27.921, -35.010451, -61.493171, -1.671108, 1.249891, -29.678548, -14.155178, -25.898, -20.681465, -31.982308, -29.475, -17.99802, -37.444193, 1.835395, -19.946, -32.769, -31.669908, -43.335452, -31.657207, -31.166046, -36.129632, -28.432407, -39.253113, -39.69377, -15.00484, -13.533583, -46.206031, -54.241577, -52.324877, -43.114821, -39.996582, -21.626126, -26.356608, -32.11613, -12.520711, -24.70893, -22.193592, -39.271322, -54.653917, -57.737657, -12.321771, -27.304796, -29.582208, -13.999186, -24.044651, -27.856554, -23.243646, -27.593092, -40.914307, -26.324073, -42.561211, -46.067939, -21.96757, -7.366428, -21.672797, -15.550401, -39.054862, -32.446847, -32.559828, -30.661621, -43.015679, -59.059625, -17.410536, -29.120334, -23.819824, -15.404188, -31.810367, -37.255412, -11.812948, -32.201389, -42.406847, -25.976942, -24.145996, -33.817763, -24.158474, -24.525933, -19.214318, -28.891602, -20.90937, -20.718913, -23.064073, -27.809136, -32.789063, -31.490397, -14.969727, -15.430935, -35.384484, -36.957709, -12.509406, -21.117242, -14.093099, -17.007039, -14.067925, -32.466905, -17.934136, -12.348958, -24.187283, -30.016005, -15.146, -13.442247, -10.817518, -6.4885, -25.776476, -18.797309, -31.424371, -27.985243, -18.782383, -16.255381, -25.660238, -13.921007, -2.528754, -10.632487, -23.141276, -11.463325, -17.799262, -24.690864, -53.685, -44.221475, -39.367, -44.370445, -36.771812, -46.454273, -36.957709, -50.453593, -30.80853, -32.580451, -23.843447, -48.496121, -45.782, -34.011264, -28.409736, -36.026062, -37.290633, -22.417028, -32.298544, -54.455385, -28.647922, -23.522, -11.420566, -14.577617, -23.742, -15.88355, -12.63799, -33.139522, -18.641145, -16.983127, -13.151332, -18.466, -15.725, -28.262566, -19.316345, -13.921455, -13.357903, -13.959917, -5.1298, -21.083, -12.901211, -4.957608, -3.227854, -31.687561, -12.808562, -24.26905, -4.000068, -18.966458, -5.3829, -17.495443, -5.6754, -22.364755, -21.337816, -21.674683, -21.794596, -31.080987, -23.670505, -35.611572, -22.047363, -16.532498, -13.023275, -30.441973, -36.005398, -29.90606, -32.90545, -33.56486, -32.102064, -30.156874, -20.715658, -32.042, -27.236274, -18.580346, -33.227, -32.683431, -28.774197, -49.695692, -34.02219, -33.993137, -36.019911, -22.194, -18.405924, -23.724189, -16.164239, -32.681207, -33.777669, -23.35612, -18.529894, -22.323785, -34.219184, -24.902832, -20.308, -30.768, -10.86398, -15.40389, -28.631836, -29.048937, -18.345052, -19.088976, -21.95025, -23.770833, -29.089, -18.683073, -12.868, -25.17, -27.761, -13.981364, -13.8699, -26.459, -7.780436, -10.965332, -8.7573, -19.734867, -7.893717, -23.922, -23.046, -9.996691, -23.440538, -24.052843, -17.546224, -25.961589, -11.777344, -36.573338, -55.735705, -43.723668, -15.668201, -38.658656, -66.332536, -46.826853, -19.749898, -47.852407, -48.430783, -58.667999, -26.688741, -44.300375, -30.670525, -41.085775, -30.478753, -59.57587, -48.794455, -48.727753, -53.679, -47.30672, -0.333333, -22.837843, -2.96776, -2.918165, 0.534081, -0.333333, -0.333333, -1.393895, -5.531937, -3.807631, -0.333333, -0.333333, -16.633538, -19.941454, -24.858914, -14.591119, -0.333333, -5.69987, -4.17277, -0.597466, -2.498542, -0.331171, -0.041951, 0.006592, -16.481, -7.653646, -6.684977, -0.177816, 0.17578, -0.34801, -8.601322, -9.645677, -0.013618, 1.6327, -1.580322, -4.819417, -5.249078, 0.12717, -0.293891, -0.333442, -0.333333, -0.162413, -4.1376, -5.857029, -1.159037, 0.046834, -0.521539, -5.351671, -2.846354, -0.33355, -11.131349, -6.6885, -4.978814, -2.804972, 0.089627, 0.452579, -5.75312, -11.193142, -0.333333, -10.858724, -6.797827, -7.421394, -6.824571, -4.563802, -0.485135, 0.032878, -4.828993, -0.537326, -0.333333, -2.879829, -10.560536, -4.13091, -7.281874, -12.339, -12.773248, -15.815213, -17.720866, -14.094998, -1.301758, -5.568793, -0.125543, 0.060126, -1.092584, -0.22385, 0.417969, -0.400228, -13.098, -9.321072, -12.275825, -1.531304, -8.157403, 0.530842, 0.587945, -0.31684, 0.274414, -12.889377, -5.894694, -9.0437, -0.425998, -0.333442, -15.287685, -5.19933, -4.7364, -3.888188, -13.713872, -5.880427, -11.180986, -1.5715, -4.398286, -12.131368, -10.550808, -10.581438, -1.4929, -6.213108, -13.505425, -5.031128, -4.929334, -6.497632, -12.916041, -13.147479, -10.248464]

class o():
  def __init__(i,**fields):
    i.override(fields)
  def override(i, d):
    i.__dict__.update(d)
    return i
  def __getattr__(i, field):
    return i.__dict__[field]
  def __setattr__(i, field, value):
    i.__dict__[field] = value
  def __repr__(i):
    d = i.__dict__
    name = i.__class__.__name__
    return name+'{'+' '.join([':%s %s' % (k,d[k])
                              for k in i.show()]) + '}'

class Point:
  def __init__(i, features, pos=None, neg=None):
    i.x = features[:-1]
    i.y = features[-1]
    if pos and neg:
      i.w = 0.5/pos if i.y == 1 else 0.5/neg
    else :
      i.w = 0
  def updateWeight(i, pos, neg):
    if i.y == 1:
      i.w = 0.5/pos
    else:
      i.w = 0.5/neg

class WeakClassifier:
  def __init__(i, points, index):
    i.x = [[point.x[index]] for point in points]
    i.y = [point.y for point in points]
    i.w = [point.w for point in points]
    i.index = index
    i.size = len(points)
    i.error = None
    i._classifier = None
    i.train()
  def train(i):
    if not i._classifier:
      i._classifier = DecisionTreeClassifier(criterion="entropy", max_depth=1, min_samples_leaf=1)
      i._classifier.fit(i.x, i.y)
  def trainError(i, start=0):
    if not i.error:
      i.error = sum([i.w[j]*abs(i.predict(i.x[j])- i.y[j]) for j in range(start, i.size)])
    return i.error
  def predict(i, inp):
    attr = inp if (len(inp) == 1) else [inp[i.index]]
    return round(i._classifier.predict(attr))
  def __repr__(i):
    return "Single Node Decision Tree" + "\n\t Index = " + str(i.index) + "\n\t Training Error = " + str(i.trainError())
  
class StrongClassifier:
  def __init__(i, mu, T, weaks=None, alphas=None):
    i.mu, i.T = mu, T
    i.weaks = [] if not weaks else weaks
    i.alphas = [] if not alphas else alphas
  def update(i, weak, alpha):
    i.weaks.append(weak)
    i.alphas.append(alpha)
  def __repr__(i):
    rep ="****Strong Classifier****\n"
    rep += "=========================\n"
    for t in range(i.T):
      rep += str(t+1)+ ") alpha = " + str(i.alphas[t])+"\n"
      rep += i.weaks[t].__repr__()
      rep += "\n\n"
    return rep
  def predict(i, inp, upper=False):
    start = math.ceil(i.T/2) if upper else 0
    LHS = sum([i.alphas[t] * i.weaks[t].predict(inp) for t in range(int(start),i.T)])
    RHS = i.mu * sum(i.alphas[int(start):])
    if LHS >= RHS:
      return  1
    return 0

class ABCD:
  def __init__(i):
    i.TP, i.FP, i.FN, i.TN = 0, 0, 0, 0
  def __repr__(i):
    rep = "\n**** Statistics ****\n"
    rep += "True  Crater     : " + str(i.TP) + "\n"
    rep += "False Crater     : " + str(i.FP) + "\n"
    rep += "False Non-Crater : " + str(i.FN) + "\n"
    rep += "True  Non-Crater : " + str(i.TN) + "\n"
    rep += "Precision        : " + str(i.precision()) + "\n"
    rep += "Recall           : " + str(i.recall()) + "\n"
    rep += "F1               : " + str(i.f1()) + "\n"
    return rep
  def update(i, pred, act):
    if pred == 0 and act == 0:
      i.TP += 1
    elif pred == 0 and act == 1:
      i.FP += 1
    elif pred == 1 and act == 0:
      i.FN += 1
    elif pred == 1 and act == 1:
      i.TN += 1
  def precision(i):
    return i.TP/(i.TP + i.FP+0.000000001)+0.000000001
  def recall(i):
    return i.TP/(i.TP + i.FN+0.000000001)+0.000000001
  def f1(i):
    return 2/(1/i.precision() + 1/i.recall())

def normalize (x):
  retx = []
  for i,val in enumerate(x):
    normalized = (val - MINS[i]) / (MAXS[i] - MINS[i])
    normalized = (val - MINS[i]) / (MAXS[i] - MINS[i])
    retx.append(normalized)
  return retx


# def max_min():
#   points = parseCSV(config.FEATURES_FOLDER+"all.csv", False)
#   maxs=[-sys.maxint]*len(points[0].x)
#   mins=[sys.maxint]*len(points[0].x)
#   for point in points:
#     for i,x in enumerate(point.x):
#       if (x<mins[i]):
#         mins[i] = x
#       if (x>maxs[i]):
#         maxs[i] = x
#   print(maxs)
#   print(mins)


def say(*lst): 
  print(*lst,end="")
  sys.stdout.flush()
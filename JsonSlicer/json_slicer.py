import json

FILE_PATH = './json/state.json.json'
SLICE_PATH = './slices/'

with open('./json/province12.json', 'r', encoding='utf8') as f:
    json_in = json.load(f)
    json_out = {}
    points = json_in['features'][0]['geometry']['coordinates']
    num_point = 0

    # 分割的文件数目
    num_slices = 10

    # 计算总点数
    for polygon in points:
        num_point += len(polygon)
    print(f.name + ' \nhas {} points in total'.format(num_point))

    # 计算每个文件包含的点数
    num_point_each_file = int(num_point / num_slices) + 1
    print('Slice into {} files, each file contains {} points'.format(num_slices, num_point_each_file))

    # 切割文件
    for num_file in range(0, num_slices):
        start = num_file * num_point_each_file
        end = (num_file + 1) * num_point_each_file

        for key in json_in:
            if key == 'features':
                json_out[key] = []
                dict_feature = {}
                for feature in json_in['features'][0]:
                    if feature == 'geometry':
                        dict_feature['geometry'] = {}
                        dict_feature['geometry']['type'] = json_in['features'][0]['geometry']['type']

                        # 针对不同的面
                        if end > len(points[0]):
                            end = len(points[0])

                        dict_feature['geometry']['coordinates'] = [[]]
                        for index in range(start, end):
                            dict_feature[feature]['coordinates'][0].append(
                                json_in['features'][0]['geometry']['coordinates'][0][index])

                        # 把其余的面放进最后一个文件
                        if num_file == num_slices - 1:
                            for j in range(1, len(points)):
                                dict_feature[feature]['coordinates'].append(
                                    json_in['features'][0]['geometry']['coordinates'][j])

                    else:
                        dict_feature[feature] = json_in['features'][0][feature]

                json_out['features'].append(dict_feature)
            else:
                json_out[key] = json_in[key]

        filename = SLICE_PATH + 'slice{}.json'.format(num_file + 1)
        with open(filename, 'w') as file:
            json.dump(json_out, file)

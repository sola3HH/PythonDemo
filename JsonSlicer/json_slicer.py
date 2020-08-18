import json
import os
import traceback
from flask import Flask, request, jsonify
from osgeo import ogr, osr

app = Flask(__name__)

app.config['FILE_PATH'] = os.path.join(app.root_path, 'json')
app.config['SLICE_PATH'] = os.path.join(app.root_path, 'slices')

"""
Tool for slicing GeoJSON into pieces
Website for test:
http://geojson.io/
https://mapshaper.org/
"""

@app.route('/slice', methods=['POST'])
def upload():
    if request.method == 'POST':
        response = {}
        try:
            f = request.files['file']
            upload_path = os.path.join(app.config['FILE_PATH'], f.filename)
            f.save(upload_path)
            # 分割的文件数目
            num_slices = int(request.form.get('slices'))
            if num_slices <= 3:
                raise Exception('at least in to 4 slices')
            area = calculate_area(upload_path)
            slice(upload_path, num_slices)
        except Exception as e:
            response['status'] = 'failed'
            response['msg'] = str(e)
            print(traceback.format_exc())
            return json.dumps(response)
        else:
            response['status'] = 'success'
            response['msg'] = 'total are: {} (10,000 m^2), into {} slices'.format(int(area), num_slices)
        return jsonify(response)


def slice(upload_path, num_slices):
    with open(upload_path, 'r', encoding='utf8') as f:
        json_in = json.load(f)
        json_out = {}

        feature_type = json_in['features'][0]['geometry']['type']

        # 几何类型为面
        if feature_type == 'Polygon':

            points = json_in['features'][0]['geometry']['coordinates']
            num_point = 0

            # 计算总点数
            for plan in points:
                num_point += len(plan)

            # 计算每个文件包含的点数
            num_point_each_file = int(num_point / (num_slices - 1)) + 1
            rest_coordinates = []

            # 切割文件
            for num_file in range(0, num_slices):
                start = num_file * num_point_each_file
                end = (num_file + 1) * num_point_each_file

                for key in json_in:
                    json_out[key] = []
                    dict_feature = {}

                    if key == 'features':
                        for feature in json_in['features'][0]:
                            if feature == 'geometry':
                                dict_feature['geometry'] = {}
                                dict_feature['geometry']['coordinates'] = [[]]

                                dict_feature['geometry']['type'] = json_in['features'][0]['geometry']['type']
                                # 如果不是最后一个文件
                                if num_file != num_slices - 1:
                                    # 针对不同的面
                                    if end > len(points[0]):
                                        end = len(points[0])

                                    for index in range(start, end):
                                        dict_feature[feature]['coordinates'][0].append(
                                            json_in['features'][0]['geometry']['coordinates'][0][index])

                                    # 把每个文件最后一个坐标放进最后一个文件里
                                    rest_coordinates.append(
                                        json_in['features'][0]['geometry']['coordinates'][0][end - 1])

                                    # 把其余的面放进最后倒数第二个文件
                                    if num_file == num_slices - 1:
                                        for j in range(1, len(points)):
                                            dict_feature['geometry']['coordinates'].append(
                                                json_in['features'][0]['geometry']['coordinates'][j])

                                # 如果是最后一个文件
                                if num_file == num_slices - 1:
                                    for rest in rest_coordinates:
                                        dict_feature['geometry']['coordinates'][0].append(rest)

                            else:
                                dict_feature[feature] = json_in['features'][0][feature]

                        json_out['features'].append(dict_feature)
                    else:
                        json_out[key] = json_in[key]

                # 输出到文件
                filename = app.config['SLICE_PATH'] + '/slice{}.json'.format(num_file + 1)
                with open(filename, 'w') as file:
                    json.dump(json_out, file)

        # # 几何类型为多面
        # if feature_type == 'MultiPolygon':
        #     for polygon in json_in['features'][0]['geometry']['coordinates']:
        #         print('Polygons : {}'.format(len(polygon[0])))
        # for polygon in json_in['features'][0]['geometry']['coordinates']:
        #     # 计算总点数
        #     num_point = 0
        #     for plan in polygon:
        #         num_point += len(plan)
        #
        #     # 计算每个文件包含的点数
        #     num_point_each_file = int(num_point / num_slices) + 1
        #
        #     # 切割文件
        #     for num_file in range(0, num_slices):
        #         start = num_file * num_point_each_file
        #         end = (num_file + 1) * num_point_each_file
        #
        #     # 针对不同的面
        #     if end > len(points[0]):
        #         end = len(points[0])
        #
        #     dict_feature['geometry']['coordinates'] = [[[]]]
        #     for index in range(start, end):
        #         dict_feature[feature]['coordinates'][polygon][0].append(
        #             json_in['features'][0]['geometry']['coordinates'][polygon][0][index])
        #
        #     # 把其余的面放进最后一个文件
        #     if num_file == num_slices - 1:
        #         for j in range(1, len(points)):
        #             dict_feature[feature]['coordinates'][polygon].append(
        #                 json_in['features'][0]['geometry']['coordinates'][polygon][j])


def calculate_area(upload_path):
    with open(upload_path, 'r', encoding='utf8') as f:
        geojson = json.load(f)
        source = osr.SpatialReference()
        source.ImportFromEPSG(4326)

        target = osr.SpatialReference()
        target.ImportFromEPSG(5243)

        transform = osr.CoordinateTransformation(source, target)
        poly = ogr.CreateGeometryFromJson(str(geojson['features'][0]['geometry']))
        poly.Transform(transform)
        return poly.GetArea()


if __name__ == '__main__':
    app.run()

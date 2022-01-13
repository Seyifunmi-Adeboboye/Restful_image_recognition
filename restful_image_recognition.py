from flask import Flask
from flask_restful import Resource, Api, reqparse
from werkzeug.datastructures import FileStorage
from Resnet50_predict import predict
import tempfile


app = Flask(__name__)
app.logger.setLevel('INFO')

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('file',
                    type=FileStorage,
                    location='files',
                    required=True,
                    help='provide a file')


class Picture(Resource):

    def post(self):
        args = parser.parse_args()
        access_file = args['file']

        pic_file, pic_name = tempfile.mkstemp()
        access_file.save(pic_name)

        pred_results = predict(pic_name)[0]

        output = {'top_categories': []}
        for _, categ, score in pred_results:
            output['top_categories'].append((categ, float(score)))

        return output


api.add_resource(Picture, '/picture')

if __name__ == '__main__':
    app.run(debug=True)

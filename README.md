ssh -i [ID_RSA] [USER]@[INSTANCE_IP]

export FLASK_APP=predict_api.py
python3 -m flask run --host=0.0.0.0 --port=5000

gulp
node dist/index.js -m spot-price-comparison -t m4.2xlarge m4.4xlarge -s 1517346477 -e 1527356577

copy spot_predictions.csv
paste unit_1.csv in AutoScalar project

run AWS.py

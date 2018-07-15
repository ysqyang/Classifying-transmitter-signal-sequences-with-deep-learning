import tensorflow as tf
import run
import argparse
import os
import numpy as np

def get_filename(data_dir, sensor_type):
    assert os.path.exists(data_dir), ('data file does not exist')
    return os.path.join(data_dir, 'predict_r{}'.format(sensor_type)) 

def input_fn(data_dir, sensor_type):
    file_name = get_filename(data_dir, sensor_type)
    # inferring batch size from total number of bytes
    total_size_in_bytes = os.path.getsize(file_name)
    batch_size = total_size_in_bytes // (run._RECORD_BYTES-1)
    sequences = np.fromfile(file_name, dtype=np.uint8)
    sequences = np.reshape(sequences, newshape=(batch_size, run._DEFAULT_SEQUENCE_LENGTH, run._NUM_CHANNELS))
    return sequences

def main(args):
    if args.sensor_type not in range(1, run._NUM_SENSOR_TYPES+1):
        print('Sensor type must be between 1 and {}'.format(run._NUM_SENSOR_TYPES))
        return
    inputs = input_fn(args.data_dir, args.sensor_type)
    with tf.Session() as sess:
        tf.saved_model.loader.load(sess, [tf.saved_model.tag_constants.SERVING], args.export_dir)
        predict_fn = tf.contrib.predictor.from_saved_model(args.export_dir)
        outputs = predict_fn({'input': inputs})
        predictions = outputs['classes']
        print('predictions: ', predictions)  

if __name__ == '__main__':  
    parser = argparse.ArgumentParser()  
    parser.add_argument('sensor_type', type=int, default=None, help='sensor type')
    parser.add_argument('--data_dir', type=str, default=os.getcwd(), help='directory to read data from')
    parser.add_argument('--export_dir', type=str, default=os.getcwd(), help='directory to load trained model from')

    args = parser.parse_args()  
  
    main(args)

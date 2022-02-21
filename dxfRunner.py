import os
import glob
from os import walk
from dxfIO import streamIO
from dxfReader import Reader
from dxfWriter import AddEntity
from arrow_reader import Arrow_Reader
import shutil


def create_empty(file_name):
    stream1 = streamIO(filename=file_name)
    stream1.create_doc()
    stream1.create_layers()
    stream1.saveDXF()


def load_create(num):
    ## create folders for dxf and json files.
    dxf_dir = './generated_dxf'
    if not os.path.isdir(dxf_dir):
        os.mkdir(dxf_dir)

    json_dir = './generated_json'
    if not os.path.isdir(json_dir):
        os.mkdir(json_dir)

    ## Create Empty dxf ground truth file
    f = []
    my_path = './raw_data'
    for (dirpath, dirnames, filenames) in walk(my_path):
        f.extend(filenames)

    for i in f:
        file_name = i.split(".")[0]  # e.g. 0030_f  0030_t  0031_f
        if file_name != "":
            try:
                view_dir = './generated_dxf/{}'.format(file_name)
                if not os.path.isdir(view_dir):
                    os.mkdir(view_dir)

                for j in range(num + 1):
                    empty_dxf_path = './generated_dxf/{}/{}_{}_0.DXF'.format(
                        file_name, file_name, j)
                    create_empty(empty_dxf_path)



                    # for k in range(7):
                    #     empty_dxf_path = './generated_dxf/{}/{}_{}_{}.DXF'.format(
                    #         file_name, file_name, j, k)
                    #     create_empty(empty_dxf_path)

                ## Read dxf info into json file
                reader_path = './raw_data/{}'.format(i)
                reader1 = Reader()
                reader1.read_dxf(reader_path)
                reader1.save_info()
                reader_save_path = './generated_json/{}.json'.format(file_name)
                reader1.save_json(reader_save_path)
            except:
                print("encounter exception")
                continue
    print("Load and Create Empty File DONE!!!")


def draw_0(file_path, json_path):
    """
    Draw everything to dxf.
    :param file_path:
    :param json_path:
    :return:
    """
    stream1 = streamIO(filename=file_path)
    stream1.load_doc()
    stream = AddEntity(stream1, json_path)

    stream.draw_contour_line()
    stream.draw_contour_circle()
    stream.draw_contour_arc()
    stream.draw_dash()
    stream.draw_construction()
    stream.draw_dimension()

    # stream.draw_bound()
    stream.draw_contour_line()
    stream1.saveDXF()


def draw_0_random(file_path, json_path):
    """
    Draw everything (random dimension) to dxf.
    :param file_path:
    :param json_path:
    :return:
    """
    stream1 = streamIO(filename=file_path)
    stream1.load_doc()
    stream = AddEntity(stream1, json_path)

    stream.draw_contour_line()
    stream.draw_contour_circle()
    stream.draw_contour_arc()
    stream.draw_dash()
    stream.draw_construction()
    stream.draw_random_dimension()

    stream.draw_contour_line()
    # stream.draw_bound()
    stream1.saveDXF()


def draw_1(file_path, json_path):
    """
    Only draw contour line
    :param file_path:
    :param json_path:
    :return:
    """
    stream1 = streamIO(filename=file_path)
    stream1.load_doc()
    stream = AddEntity(stream1, json_path)

    stream.draw_contour_line()

    # stream.draw_bound()
    stream1.saveDXF()


def draw_2(file_path, json_path):
    """
    Only draw contour circle
    :param file_path:
    :param json_path:
    :return:
    """
    stream1 = streamIO(filename=file_path)
    stream1.load_doc()
    stream = AddEntity(stream1, json_path)

    stream.draw_contour_circle()

    # stream.draw_bound()
    stream1.saveDXF()


def draw_3(file_path, json_path):
    """
    Only draw contour arc
    :param file_path:
    :param json_path:
    :return:
    """
    stream1 = streamIO(filename=file_path)
    stream1.load_doc()
    stream = AddEntity(stream1, json_path)

    stream.draw_contour_arc()

    # stream.draw_bound()
    stream1.saveDXF()


def draw_4(file_path, json_path):
    """
    Only draw contour dash
    :param file_path:
    :param json_path:
    :return:
    """
    stream1 = streamIO(filename=file_path)
    stream1.load_doc()
    stream = AddEntity(stream1, json_path)

    stream.draw_dash()

    # stream.draw_bound()
    stream1.saveDXF()


def draw_5(file_path, json_path):
    """
    Only draw construction
    :param file_path:
    :param json_path:
    :return:
    """
    stream1 = streamIO(filename=file_path)
    stream1.load_doc()
    stream = AddEntity(stream1, json_path)

    stream.draw_construction()

    # stream.draw_bound()
    stream1.saveDXF()


def draw_6(file_path, json_path):
    """
    Only draw dimensions
    :param file_path:
    :param json_path:
    :return:
    """
    stream1 = streamIO(filename=file_path)
    stream1.load_doc()
    stream = AddEntity(stream1, json_path)

    stream.draw_dimension()

    # stream.draw_bound()
    stream1.saveDXF()


def draw_6_random(file_path, json_path):
    """
    Only draw contour line
    :param file_path:
    :param json_path:
    :return:
    """
    stream1 = streamIO(filename=file_path)
    stream1.load_doc()
    stream = AddEntity(stream1, json_path)

    stream.draw_random_dimension()

    # stream.draw_bound()
    stream1.saveDXF()


def draw_contour_wo_dash(file_path, json_path):
    stream1 = streamIO(filename=file_path)
    stream1.load_doc()
    stream = AddEntity(stream1, json_path)
    stream.draw_contour()
    # stream.draw_bound()
    stream1.saveDXF()


def draw_contour_w_dash(file_path, json_path):
    stream1 = streamIO(filename=file_path)
    stream1.load_doc()
    stream = AddEntity(stream1, json_path)
    stream.draw_contour()
    stream.draw_dash()
    # stream.draw_bound()
    stream1.saveDXF()


def draw_whole(file_path, json_path):
    stream1 = streamIO(filename=file_path)
    stream1.load_doc()
    stream = AddEntity(stream1, json_path)
    stream.draw_contour()
    stream.draw_dash()
    stream.draw_construction()
    stream.draw_dimension()
    # stream.draw_bound()
    stream1.saveDXF()


def draw_random(file_path, json_path):
    stream1 = streamIO(filename=file_path)
    stream1.load_doc()
    stream = AddEntity(stream1, json_path)
    stream.draw_contour()
    stream.draw_dash()
    stream.draw_construction()
    stream.draw_random_dimension()
    # stream.draw_bound()
    stream1.saveDXF()


def draw(num):
    json_file = []
    json_path = './generated_json'
    for (dirpath, dirnames, filenames) in walk(json_path):
        json_file.extend(filenames)

    for json in json_file:  ## json file for each view.
        try:
            view_name = json.split(".")[0]  # 0115_f    0131_t
            json_path_to_load = './generated_json/{}'.format(json)

            dxf_file = []
            dxf_path = './generated_dxf/{}'.format(view_name)
            for (dirpath2, dirnames2, filenames2) in walk(dxf_path):
                dxf_file.extend(filenames2)

            print("Working on ... ", view_name)
            for file in dxf_file:
                origin_file_name = view_name + '_0'
                if file.startswith(origin_file_name):
                    if file.endswith('0.DXF'):
                        file_to_write_name = origin_file_name + '_0'
                        file_path_to_write = './generated_dxf/{}/{}.DXF'.format(
                            view_name, file_to_write_name)
                        draw_0(file_path_to_write, json_path_to_load)
            
                for n in range(1, num + 1):
                    new_file_name = view_name + '_' + str(n)
                    if file.startswith(new_file_name):
                        if file.endswith('0.DXF'):
                            file_to_write_name = new_file_name + '_0'
                            file_path_to_write = './generated_dxf/{}/{}.DXF'.format(
                                view_name, file_to_write_name)
                            draw_0_random(file_path_to_write, json_path_to_load)

            print(view_name, " is done.")
        except:
            continue
    print("Draw File DONE!!!")


def copy():
    delete_set = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '10'}
    origin_dir = './generated_dxf'
    dest = './dxf_tobe_converted'
    if not os.path.isdir(dest):
        os.mkdir(dest)
    dirs = os.listdir(origin_dir)
    for folder in dirs:
        origin_dxf_dir = origin_dir + '/{}'.format(folder)
        src_files = os.listdir(origin_dxf_dir)
        for file_name in src_files:
            checker = file_name.split('_')[2]
            if checker in delete_set:
                continue

            full_file_name = os.path.join(origin_dxf_dir, file_name)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, dest)

    print("Copy File DONE!!!")



def arrow_handle():
    ## create arrow_folder for json which contains arrow info
    arrow_dir = './arrow_json_garbage'

    if not os.path.isdir(arrow_dir):
        os.mkdir(arrow_dir)

    
    path = glob.glob('./dxf_tobe_converted/*.DXF')
    for f in path:
        if f.endswith('6.DXF'):
            file_name = os.path.basename(f).split('.')[0][:-1]
            save_path = arrow_dir + '/' + file_name + '0.json'

            reader = Arrow_Reader()
            reader.read_dxf(f)
            reader.save_info()
            reader.save_json(save_path)
    
    print("Save Arrow Info Done!!!")




if __name__ == "__main__":
    num = 10
    load_create(num)
    draw(num)
    copy()
    # arrow_handle()

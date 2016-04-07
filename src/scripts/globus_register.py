import argparse
import os
from globusonline.catalog.client.catalog_wrapper import *
from globusonline.catalog.client.operators import Op
from globusonline.catalog.client.rest_client import RestClientError


def register_file(ipts, filename, sample, temperature):
    # Store authentication data in a local file
    token_file = os.getenv('HOME','')+"/.ssh/gotoken.txt"
    wrap = CatalogWrapper(token_file=token_file)
    gcat = wrap.catalogClient

    _, catalogs = wrap.catalogClient.get_catalogs()
    for catalog in catalogs:
        if catalog['config']['name'] == 'SNS-Demo-1:
            catalog_id = catalog['id']

    _, datasets = wrap.catalogClient.get_datasets(catalog_id)
    dataset_id = None
    for dataset in datasets:
        if dataset['name'] == sample:
            dataset_id = dataset['id']
    if dataset_id is None:
        dataset_info = {"name":sample}
        _,response = gcat.create_dataset(catalog_id, dataset_info)
        dataset_id = response['id']

    member_info = {"data_type":"file", "data_uri":filename}
    _,response = gcat.create_member(catalog_id, dataset_id, member_info)
    member_id = response['id']
    
    new_annotations = [ {"name":"temperature", "type":"float8"},
                        {"name":"sample", "type":"text"}, 
                        {"name":"ipts", "type":"int8"},
                        {"name":"facility", "type":"text"]
    responses = []
    for annotation in new_annotations:
        _,response = gcat.create_annotation_def(catalog_id, annotation['name'],annotation['type'])
        responses.append(response)    

    _,response = gcat.add_dataset_annotations(catalog_id, dataset_id, 
                     {"temperature":temperature, 
                      "sample":sample,
                      "ipts:":ipts,
                      "facility":"SNS"})

def main():

    parser = argparse.ArgumentParser(
        description="Create NeXus file for diffuse scattering")
    parser.add_argument('-i', '--ipts', default='14374', help='IPTS Number')
    parser.add_argument('-f', '--file', default='PMN35PT_006K_norm', help='name of NeXus file')
    parser.add_argumnet('-s', '--sample', default='PMN35PT', help='name of sample')
    parser.add_argument('-t', '--temperature', default='6.0', help='sample temperature')
    args = parser.parse_args()

    ipts = args.ipts
    directory = '/SNS/CORELLI/IPTS-%s' % ipts
    if len(args.runs) == 2:
        runs = range(args.runs[0], args.runs[1]+1)
    else:
        runs = args.runs
    filename = os.path.join(directory, 'shared', args.file + '.nxs')
    sample = args.sample
    temperature = float(args.temperature)

    register_file(ipts, filename, sample, temperature)

if __name__ == '__main__':
    main()

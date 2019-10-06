# Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# This file is licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License. A copy of the
# License is located at
#
# http://aws.amazon.com/apache2.0/
#
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
# OF ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import boto3
from botocore.exceptions import ClientError
import os
from siteconfig.globals import S3_USER_ACCESS_ID, S3_USER_SECRET
import logging
from django.conf import settings

BUCKET_NAME = settings.AWS_BUCKET

s3_client = boto3.client('s3', aws_access_key_id=S3_USER_ACCESS_ID, aws_secret_access_key=S3_USER_SECRET)
session = boto3.Session(
    region_name='us-west-1',
    aws_access_key_id=S3_USER_ACCESS_ID,
    aws_secret_access_key=S3_USER_SECRET,
)
resource = session.resource('s3')

def transfer_file(src_bucket, src_path, dst_bucket):
    s3 = session.resource('s3')
    copy_source = {
        'Bucket': src_bucket,
        'Key': src_path,
    }

    s3.meta.client.copy(copy_source, dst_bucket, src_path)

def get_object(bucket_name, object_name):
    """Retrieve an object from an Amazon S3 bucket

    :param bucket_name: string
    :param object_name: string
    :return: botocore.response.StreamingBody object. If error, return None.
    """

    # Retrieve the object
    s3 = boto3.client('s3')
    try:
        response = s3.get_object(Bucket=bucket_name, Key=object_name)
    except ClientError as e:
        # AllAccessDisabled error == bucket or object not found
        logging.error(e)
        return None
    # Return an open StreamingBody object
    print(response)
    return response['Body']

def put_object(dest_bucket_name, dest_object_name, src_data):
    """Add an object to an Amazon S3 bucket

    The src_data argument must be of type bytes or a string that references
    a file specification.

    :param dest_bucket_name: string
    :param dest_object_name: string
    :param src_data: bytes of data or string reference to file spec
    :return: True if src_data was added to dest_bucket/dest_object, otherwise
    False
    """

    # Construct Body= parameter
    if isinstance(src_data, bytes):
        object_data = src_data
    elif isinstance(src_data, str):
        try:
            object_data = open(src_data, 'rb')
            # possible FileNotFoundError/IOError exception
        except Exception as e:
            logging.error(e)
            return False
    else:
        logging.error('Type of ' + str(type(src_data)) +
                      ' for the argument \'src_data\' is not supported.')
        return False

    try:
        s3_client.put_object(Bucket=dest_bucket_name, Key=dest_object_name, Body=object_data)
    except ClientError as e:
        # AllAccessDisabled error == bucket not found
        # NoSuchKey or InvalidRequest error == (dest bucket/obj == src bucket/obj)
        logging.error(e, exc_info=True)
        return False
    finally:
        if isinstance(src_data, str):
            object_data.close()
    return True


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then same as file_name
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def get_location(bucket_name):
    bucket_location = s3_client.get_bucket_location(Bucket=bucket_name)
    return bucket_location

def download_link(s3_file_path, output_file_path):
    s3 = boto3.client('s3')
    s3.download_file(BUCKET_NAME, s3_file_path, output_file_path)

def create_article_url(blog_name, article_id):
    location = get_location(BUCKET_NAME)['LocationConstraint']

    object_url = "https://s3-{bucket_location}.amazonaws.com/{bucket_name}/{blog_name}/{article_id}.html".format(
        bucket_location=location,
        bucket_name=BUCKET_NAME,
        blog_name=blog_name,
        article_id=article_id
    )

    return object_url

def create_pdf_url(bucket_name, blog_name, article_id):
    location = get_location(bucket_name)['LocationConstraint']

    object_url = "https://s3-{bucket_location}.amazonaws.com/{bucket_name}/{blog_name}/{article_id}.pdf".format(
        bucket_location=location,
        bucket_name=bucket_name,
        blog_name=blog_name,
        article_id=article_id
    )

    return object_url


def upload_article(blog_name, article_id, content, bucket_name=BUCKET_NAME):
    id_path = '{}.html'.format(article_id)
    try:
        os.mkdir(os.path.join('dump', blog_name))
    except:
        pass
    local_path = os.path.join('dump', blog_name, id_path)

    with open(local_path, 'w') as f:
        f.write(str(content))
    f.close()

    put_object(dest_bucket_name=bucket_name, dest_object_name=os.path.join(blog_name, id_path), src_data=local_path)

def check_file(path, bucket_name=BUCKET_NAME):

    try:
        resource.Object(bucket_name, path).load()
        return True
    except ClientError as e:
        logging.error(e, exc_info=True)
        if e.response['Error']['Code'] == "404":
            return False

def delete_file(bucket_name, path):

    s3 = boto3.resource('s3')
    s3.Object(bucket_name, path).delete()

def clear_all(bucket_name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.objects.all().delete()
    logging.debug("Cleared out %s S3 Bucket", bucket_name)
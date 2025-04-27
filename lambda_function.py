import boto3
from pyiceberg.catalog import load_catalog
import pyarrow as pa

region = 'us-west-2'
s3tables = boto3.client('s3tables')
table_buckets = s3tables.list_table_buckets(maxBuckets=1000)['tableBuckets']
catalog_map = {}
for table_bucket in table_buckets:
    name = table_bucket['name']
    arn = table_bucket['arn']
    rest_catalog = load_catalog(
        "catalog_name",
        **{
            "type": "rest",
            "warehouse":arn,
            "uri": f"https://s3tables.{region}.amazonaws.com/iceberg",
            "rest.sigv4-enabled": "true",
            "rest.signing-name": "s3tables",
            "rest.signing-region": region,
            "py-io-impl": "pyiceberg.io.fsspec.FsspecFileIO"
        }
    )
    catalog_map[name] = rest_catalog
def handler(event, context):
    # 从事件中获取表名
    table_name = event['table_name']
    namespace = event['namespace']
    bucket_name = event['bucket_name']
    rest_catalog = catalog_map[bucket_name]
    # 从事件中获取要插入的数据
    insert_data = event['insert_data']
    # 查询表
    table = rest_catalog.load_table(namespace+'.'+table_name)
    df = pa.Table.from_pylist(
        insert_data, schema=table.schema().as_arrow()
    )
    # 插入表
    table.append(df)
    return {
        'statusCode': 200,
        'body': ''
    }
# 测试
# event = {
#     'table_name': 'test_table',
#     'namespace': 'namespace_example',
#     'bucket_name': 'testtable',
#     'insert_data': [
#         {"id": 306, "data": 'test insert icb 1'},
#         {"id": 307, "data": 'test insert icb 2'}
#     ]
# }
# handler(event, None)
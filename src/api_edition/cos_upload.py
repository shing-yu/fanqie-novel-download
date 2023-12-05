# noinspection PyPackageRequirements
from qcloud_cos import CosConfig
# noinspection PyPackageRequirements
from qcloud_cos import CosS3Client
import os


def cos_upload(file_path):
    # 检查配置文件
    if os.path.exists("cos-config.json"):
        # 读取配置文件
        import json
        with open("cos-config.json", "r") as f:
            config = json.load(f)
        try:
            secret_id = config["secret_id"]
            secret_key = config["secret_key"]
            region = config["region"]
            bucket = config["bucket"]
            if "token" in config:
                token = config["token"]
            else:
                token = None
            if "scheme" in config:
                scheme = config["scheme"]
            else:
                scheme = "https"
        except KeyError:
            raise KeyError("配置文件格式不正确")
    else:
        # 如果没有配置文件，则从环境变量中获取配置
        secret_id = os.getenv("TC_SECRET_ID")  # 替换为用户的 secretId
        secret_key = os.getenv("TC_SECRET_KEY")  # 替换为用户的 secretKey
        region = os.getenv("COS_REGION")  # 替换为用户的 Region
        bucket = os.getenv("COS_BUCKET")  # 替换为用户的 Bucket
        token = os.getenv("COS_SESSION_TOKEN", None)  # 使用临时密钥需要传入 Token，默认为空，可不填
        scheme = os.getenv("COS_SCHEME", "https")  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
        assert "-" in bucket, "环境变量 COS_BUCKET 的格式不正确"

    # 检查配置的值
    assert secret_id is not None, "请设置环境变量 TC_SECRET_ID"
    assert secret_key is not None, "请设置环境变量 TC_SECRET_KEY"
    assert region is not None, "请设置环境变量 COS_REGION"
    assert bucket is not None, "请设置环境变量 COS_BUCKET"

    assert scheme in ["http", "https"], "环境变量 COS_SCHEME 的值必须为 http 或 https（不设置为 https）"

    # 设置用户属性, 包括 secretId, secretKey, region 以及 token
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
    # 生成客户端对象
    client = CosS3Client(config)

    # 获取文件名
    file_name = os.path.basename(file_path)
    # 拼接cos路径
    cos_base_dir = os.getenv("COS_BASE_DIR", "")
    cos_dir = "番茄小说"
    # cos不需要使用os.path.join
    object_name = cos_base_dir + cos_dir + "/" + file_name

    # 上传文件
    response = client.upload_file(
        Bucket=bucket,
        LocalFilePath=file_path,
        Key=object_name,
        EnableMD5=True
    )

    return response["ETag"]


if __name__ == "__main__":
    print("测试上传文件")
    cos_upload("test.txt")

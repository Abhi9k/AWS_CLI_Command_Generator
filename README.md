# AWS_CLI_Command_Generator #
Converts a JSON string or a Python dictionary containing options of AWS CLI into a valid CLI command string.
## Usage ##

1. As a standalone script

    python aws_cli_manager.py [aws service name] [service command name] [valid json string containing options]

      For example:
      >python aws_cli_manager.py ec2 run-instances '{"image-id":"some image id","instance-type":"t2.small","dry-run":"","tag-specifications":[{"ResourceType":"instance","Tags":[{"Key":"Name","Value":"myserver"}]}]}'

      Here is a prettified version of options json used above. Please note for using it with script, the json string should be a one long string.

      ```json
      {
        "image-id": "some image id",
        "instance-type": "t2.small",
        "dry-run": "",
        "tag-specifications": [
          {
            "ResourceType": "instance",
            "Tags": [
              {
                "Key": "Name",
                "Value": "my server"
              }
            ]
          }
        ]
      }
      ```

      Output:

      **aws ec2 run-instances --tag-specifications 'ResourceType=instance,Tags=[{Value=myserver,Key=Name}]' --instance-type t2.small --dry-run  --image-id some image id**

2. Inside another script

    import aws_cli_manager.py as AWS_CLI_MANAGER
    1. AWS_CLI_MANAGER.generate_aws_cli_command([aws service name],[service command name],[valid json string containing options])
    or
    2. AWS_CLI_MANAGER.generate_aws_cli_command([aws service name],[service command name], [python dictionary containing options]

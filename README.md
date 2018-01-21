# AWS_CLI_Command_Generator #
Converts a JSON string or a Python dictionary containing options of AWS CLI into a valid CLI command string.
## Usage ##
python aws_cli_manager.py [aws service name] [service command name] [valid json string containing options]

  For example:
  >python aws_cli_manager.py ec2 run-instances '{"image-id":"some image id","instance-type":"t2.small","dry-run":"","tag-specifications":[{"ResourceType":"instance","Tags":[{"Key":"Name","Value":"myserver"}]}]}'

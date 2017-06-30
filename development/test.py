import yaml

async def test(cmd, message, args):
    with open(cmd.resource('test.yml')) as test_file:
        data = yaml.safe_load(test_file)
    await message.channel.send('OK.')

const { SlashCommandBuilder } = require('discord.js');
const { PythonShell } = require('python-shell');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('prevent-low')
		.setDescription('See tips how to prevent low blood pressure.'),
	async execute(interaction) {
        await interaction.reply({content: 'Working on it', ephemeral:true});
        const result = await pythonCall();
        await interaction.followUp({content: result.join("\n"), ephemeral:true});
	},
};

function pythonCall(){
    return new Promise(resolve => {
      PythonShell.run('./python/prevent-low.py', {pythonOptions: ['-u']}, function (err,result) {
        if (err) throw err;
        // console.log(result)
        resolve(result);
      })
    })
  }
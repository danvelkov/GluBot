const { SlashCommandBuilder } = require('discord.js');
const { PythonShell } = require('python-shell');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('upload')
		.setDescription('Upload csv file with glucose readings')
        .addAttachmentOption((option)=> option
            .setRequired(true)
            .setName("csv_file")
            .setDescription("The image to dither")),
	async execute(interaction) {
        const attachment = interaction.options.getAttachment("csv_file")
        const name = attachment.name
        // const proxyURL = attachment.proxyURL
        
        var re = /(?:\.([^.]+))?$/;
        var ext = re.exec(name)[1];

        if(ext == "csv"){
        const url = attachment.url

        await interaction.reply({content: 'Working on it', ephemeral:true});
        const result = await pythonCall(url);
        await interaction.followUp({content: result.join("\n"), ephemeral:true});
        } else {
          await interaction.reply({content: 'File is not .csv\nPlease upload a .csv file!', ephemeral:true});
        }
	},
};

function pythonCall(file){
    return new Promise(resolve => {
      PythonShell.run('./python/data-analysis.py', {args: file, pythonOptions: ['-u']}, function (err,result) {
        if (err) throw err;
        // console.log(result)
        resolve(result);
      })
    })
  }
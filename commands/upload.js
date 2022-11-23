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
        const url = attachment.url
        const proxyURL = attachment.proxyURL
        // console.log("response " + String(await pythonCall(url)))
		// await interaction.reply({content: name + " " + url + " " + proxyURL, ephemeral:true});

        // await interaction.reply({content: String(await pythonCall(url)), ephemeral:true});
        // await interaction.deferReply();
        // const result = await reply();
        // await interaction.editReply(result);
        await interaction.reply({content: 'Working on it', ephemeral:true});
        const result = await pythonCall(url);
        await interaction.followUp({content: String(result), ephemeral:true});
	},
};

// async function reply(result) {
//     await interaction.reply({content: String(result), ephemeral:true});
// }

function pythonCall(file){
    return new Promise(resolve => {
      PythonShell.run('./python/data-analysis.py', {args: file, pythonOptions: ['-u']}, function (err,result) {
        if (err) throw err;
        // console.log(result);
        resolve(result);
      })
    })
  }
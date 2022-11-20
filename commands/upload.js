const { SlashCommandBuilder } = require('discord.js');

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

		await interaction.reply(name + " " + url + " " + proxyURL);
	},
};
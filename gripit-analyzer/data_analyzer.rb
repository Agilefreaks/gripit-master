#!/usr/bin/env ruby
require 'pathname'
require 'csv'

READINGS_DIR_NAME = 'readings'
CONSOLIDATED_READINGS_FILE_NAME = 'consolidated_readings.csv'

READINGS_DIR = Dir.new('readings')
READINGS_DIR_PATH = File.absolute_path(READINGS_DIR.path)
READING_FILES = READINGS_DIR.entries.select { |entry| entry.end_with?('.csv') }.reverse
CONSOLIDATED_READINGS_FILE_PATH = File.expand_path(CONSOLIDATED_READINGS_FILE_NAME)

def show_reading_summary(reading_index)
    file_name = READING_FILES[reading_index - 1]
    readings = CSV.foreach(File.join(READINGS_DIR_PATH, file_name)).map { |row| row[2].to_i }

    puts "filename is          : #{file_name}"
    puts "total readings count : #{readings.size}"
    puts "average is           : #{readings.reduce(:+) / readings.size.to_f}"
    puts "max is               : #{readings.max}"
    puts "min is               : #{readings.min}"
end

def consolidate_readings(indexes)
    CSV.open(CONSOLIDATED_READINGS_FILE_PATH, 'wb') do |csv|
        indexes = indexes.empty? ? (1..READING_FILES.count).to_a : indexes
        files_to_consolidate = READING_FILES.select.with_index { |_, index| indexes.include?(index + 1) }
        csv << files_to_consolidate
        consolidated_data = []
        files_to_consolidate
            .map { |file_name| File.join(READINGS_DIR_PATH, file_name) }
            .map { |f| CSV.read(f) }
            .each_with_index do |readings, file_index|
            readings.each_with_index do |reading, reading_index|
                consolidated_data[reading_index] = consolidated_data[reading_index] || []
                consolidated_data[reading_index][file_index] = reading[2]
            end
        end
        consolidated_data.each { |entry| csv << entry }
    end
end

case ARGV[0]
    when '-f'
        show_reading_summary(ARGV[1].to_i)
    when '-c'
        consolidate_readings(ARGV[1].to_s.split(',').map(&:to_i))
    else
        puts 'Usage: ./data_analyzer.rb [-f 15] [-c [1],[2]]'
end

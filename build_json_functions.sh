#!/bin/bash

for file in $(ls ./mycroft-json-messages/ | grep ".json");do
	./template_function "./mycroft-json-messages/${file}";
done

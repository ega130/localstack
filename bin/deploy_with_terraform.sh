#!/bin/bash

zip lambda_function.zip lambda_function.py
terraform apply -auto-approve
# this docker fixes a issue with the existing docker container 
# where there was a compatibitly issue with reachy 1.2.3 with the pylous module 
# fix was the  grading the version to reachy 1.3.2 
# pip install reachy==1.3.2 
FROM ekkus93/reachy-docker:latest
LABEL maintainer="oranbusiness@gmail.com"
# activate the prebuild conda python enviorment so pip  correctly installs
# in the right place
# SHELL ["/bin/bash", "--login", "-c"]

# # conda requires shell to be initalized to run conda commands
# # SHELL ["conda", "init", "reachy-env","&&","pip","uninstall","reachy","&&","pip","uninstall","reachy","/bin/bash", "-c"]
# # remove the existing reachy package
# RUN pip uninstall reachy
# # install the fixed and correct version number
# RUN pip install reachy==1.3.2

COPY environment.yml .
# RUN conda env create -f environment.yml
RUN conda env update --file environment.yml
# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "reachy-env", "/bin/bash", "-c"]

# Make sure the environment is activated:
RUN echo "Make sure flask is installed:"
RUN python -c "import reachy"
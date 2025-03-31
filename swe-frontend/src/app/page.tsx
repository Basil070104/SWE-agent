'use client'
import Image from "next/image";
import ReactMarkdown from 'react-markdown';
import { motion } from "motion/react"
import { useState, useEffect } from "react"

export default function Home() {
  const markdown = `1:# coding=utf-8
2:# Copyright 2023 The HuggingFace Inc. team.
3:#
4:# Licensed under the Apache License, Version 2.0 (the "License");
5:# you may not use this file except in compliance with the License.
6:# You may obtain a copy of the License at
7:#
8:#     http://www.apache.org/licenses/LICENSE-2.0
9:#
10:# Unless required by applicable law or agreed to in writing, software
11:# distributed under the License is distributed on an "AS IS" BASIS,
12:# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
13:# See the License for the specific language governing permissions and
14:# limitations under the License.
15:
16:import argparse
17:import copy
18:import logging
19:import math
20:import os
21:import shutil
22:from contextlib import nullcontext
23:from pathlib import Path
24:
25:import torch
26:import torch.nn.functional as F
27:from accelerate import Accelerator
28:from accelerate.logging import get_logger
29:from accelerate.utils import ProjectConfiguration, set_seed
30:from datasets import load_dataset
31:from peft import LoraConfig
32:from peft.utils import get_peft_model_state_dict
33:from PIL import Image
34:from PIL.ImageOps import exif_transpose
35:from torch.utils.data import DataLoader, Dataset, default_collate`;

  const [data, setdata] = useState({
    name: "",
    age: 0,
    date: "",
    programming: "",
  });

  useEffect(() => {
    // Using fetch to fetch the api from 
    // flask server it will be redirected to proxy
    fetch("/data").then((res) =>
      res.json().then((data) => {
        setdata({
          name: data.Name,
          age: data.Age,
          date: data.Date,
          programming: data.programming,
        });
      })
    );
  }, []);


  return (
    <div className="flex items-center justify-center h-screen max-h-screen w-screen">
      <main className="w-4/5 h-9/10">
        {/* Header */}
        <div className="flex flex-row justify-center items-center">
          <div className="bg-gray-400 grow h-0.5 mr-4 rounded-md"></div>
          <div className="text-4xl flex-none font-exo">
            SWE-agent
          </div>
          <div className="bg-gray-400 grow h-0.5 ml-4 rounded-md"></div>
        </div>
        <div className="text-lg font-exo">
          v1 - Branch : main
        </div>
        <div className="bg-gray-400 grow h-0.5 mt-4 rounded-md"></div>
        {/* Information */}
        <div className="grid gap-4 grid-cols-2 grid-rows-2 grid-flow-col-dense h-3/4 p-4">
          {/* Workspace */}
          <div className="row-span-2 rounded-md h-full overflow-hidden">
            <div className="flex flex-row">
              <Image
                src="/images/workspace.png"
                alt="Workspace"
                height={20}
                width={25}
              />
              <div className="mx-4 font-exo">
                Workspace
              </div>
            </div>
            <div className="w-full h-full pt-2">
              <div className="bg-white w-full h-full rounded-md text-black p-4 font-exo text-wrap whitespace-pre-line">
                {data.name}

              </div>
            </div>
          </div>
          {/* Editor */}
          <div className=" rounded-md h-full overflow-hidden">
            <div className="flex flex-row">
              <Image
                src="/images/editor.png"
                alt="Editor"
                height={20}
                width={25}
              />
              <div className="mx-4 font-exo">
                Editor
              </div>
            </div>
            <div className="w-full h-full pt-2">
              <div className="bg-white w-full h-full rounded-l-md p-4 text-black font-exo overflow-y-auto whitespace-pre-line">
                {markdown}

              </div>
            </div>
          </div>
          {/* Terminal */}
          <div className=" rounded-md h-full overflow-hidden">
            <div className="flex flex-row">
              <Image
                src="/images/terminal.png"
                alt="Terminal"
                height={20}
                width={25}
              />
              <div className="mx-4 font-exo">
                Terminal
              </div>
            </div>
            <div className="w-full h-full pt-2">
              <div className="bg-white w-full h-full rounded-l-md font-exo text-black p-4">
                <div>
                  $
                </div>
                <div className="bg-gray-300 grow h-0.5 mt-1 rounded-md"></div>
              </div>
            </div>
          </div>
        </div>
        <div className="flex flex-row w-full justify-around items-center font-exo">

          <motion.div className="bg-gray-300 text-black py-2 px-4 rounded-md cursor-pointer"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            Reset
          </motion.div>

          <motion.div className="bg-gray-300 text-black py-2 px-6 rounded-md cursor-pointer"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            Next Step
          </motion.div>
        </div>
        <div className="bg-gray-300 grow h-0.5 mt-4 rounded-md"></div>
        <div className="flex w-full justify-center items-center m-4 font-exo">
          Created by Basil Khwaja
        </div>
      </main>

    </div>
  );
}

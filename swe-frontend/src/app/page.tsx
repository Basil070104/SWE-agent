'use client'
import Image from "next/image";
// import ReactMarkdown from 'react-markdown';
import { motion } from "motion/react"
import { useState, useEffect, useRef } from "react"
import { AxiosResponse } from 'axios';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { prism } from "react-syntax-highlighter/dist/esm/styles/prism";
// import { Axios } from "axios";

export default function Home() {

  const axios = require('axios').default;
  const API_BASE_URL = 'http://127.0.0.1:5000'

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

  const [data, setData] = useState({
    name: "",
    age: 0,
    date: "",
    programming: "",
  });

  const [git, setGit] = useState("")
  const [query, setQuery] = useState("")
  const [workspace, setWorkspace] = useState("")
  const [director, setDirectory] = useState("")
  const [terminal, setTerminal] = useState("")
  const [description, setDescription] = useState("")
  const pollingIntervalRef = useRef<NodeJS.Timeout | null>(null);;

  useEffect(() => {
    // Poll for terminal updates every 1 second
    pollingIntervalRef.current = setInterval(fetchTerminalUpdates, 1000);

    return () => {
      if (pollingIntervalRef.current) {
        clearInterval(pollingIntervalRef.current);
      }
    };
  }, []);

  const fetchTerminalUpdates = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/terminal_updates`);
      console.log(response.data)
      if (response.data && response.data.length > 0) {
        setTerminal(response.data.command);
        setDescription(response.data.description);
      }
    } catch (error) {
      console.error('Error fetching terminal updates:', error);
    }
  };

  const appendToWorkspace = (newContent: any) => {
    setWorkspace((prevWorkspace) => prevWorkspace + newContent + "<hr />"); // Append new content
  };

  const handleSubmit = (query: string) => {
    console.log("Submitted query:", query);
    setGit(query);

    axios.post('http://127.0.0.1:5000/git_clone', { url: query }) // Send POST request
      .then((response: AxiosResponse) => {
        console.log("Response from server:", response.data);
        const data = response.data
        console.log(data.data);
        appendToWorkspace(`${data.data.repo_path} \n${response.status}\n`)
      })
      .catch((error: any) => {
        console.error("Error sending query:", error); // Handle error
      });

    // axios.post('http://127.0.0.1:5000/git_issue', { url: query }) // Send POST request
    //   .then((response: AxiosResponse) => {
    //     console.log("Response from server:", response.data);
    //     const data = response.data
    //     console.log(data.data);
    //     // appendToWorkspace(`${data.data.repo_path} \n${response.status}\n`)
    //   })
    //   .catch((error: any) => {
    //     console.error("Error sending query:", error); // Handle error
    //   });


  }

  const reset = () => {
    console.log("Resetting...")
  }
  return (
    <div className="flex items-center justify-center h-screen max-h-screen w-screen overflow-x-hidden">
      <main className="w-4/5 h-9/10">
        {/* Header */}
        <div className="flex flex-row justify-center items-center">
          <div className="bg-gray-400 grow h-0.5 mr-4 rounded-md"></div>
          <div className="text-4xl flex-none font-exo">
            SWE-agent
          </div>
          <div className="bg-gray-400 grow h-0.5 ml-4 rounded-md"></div>
        </div>
        <div className="text-lg font-exo flex flex-row py-2 items-center">
          <div>
            v1
          </div>
          <div className="px-4 w-fit">
            Query
          </div>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              if (query.trim()) {
                handleSubmit(query);
                setQuery('');
              }
            }}
            className="w-full flex flex-row items-center gap-2"
          >
            <input
              type="text"
              placeholder="Enter your issue url"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent"
              aria-label="Command input"
              required
            />
            <button
              type="submit"
              className="bg-amber-500 text-white font-medium rounded px-4 py-2 hover:bg-amber-700 transition-colors "
              disabled={!query.trim()}
            >
              Submit
            </button>
          </form>
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
              <div className="bg-white w-full h-full rounded-md  p-4 font-exo text-wrap whitespace-pre-line" >
                <pre dangerouslySetInnerHTML={{ __html: workspace }} className="text-wrap text-black [&>hr]:mt-2">

                </pre>
                {/* {workspace} */}
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
            <div className="w-full h-full rounded-md overflow-y-auto mt-2" style={{ maxHeight: '400px', paddingBottom: '20px', backgroundColor: '#f5f5f5' }}>
              <SyntaxHighlighter
                language="python"
                style={prism}
                customStyle={{
                  marginBottom: 10,
                  borderRadius: '5px', // Add rounded corners
                  padding: '10px', // Add padding inside the highlighter
                  backgroundColor: 'transparent' // Ensure background is transparent or set to desired color
                }}
              >
                {markdown}
              </SyntaxHighlighter>
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
                <div className="flex flex-row">
                  <div>
                    $
                  </div>
                  <pre className="mx-2 text-wrap">
                    {terminal}
                  </pre>
                </div>
                <div className="bg-gray-300 grow h-0.5 mt-1 rounded-md"></div>
                <div>
                  {description}
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="flex flex-row w-full justify-around items-center font-exo">

          <motion.div className="bg-amber-500 text-white py-2 px-4 rounded-md cursor-pointer"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            Reset
          </motion.div>

          <motion.div className="bg-amber-500 text-white py-2 px-6 rounded-md cursor-pointer"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            Pull Request
          </motion.div>
        </div>
        <div className="bg-gray-300 grow h-0.5 mt-4 rounded-md"></div>
        <a href="https://github.com/Basil070104" target="_blank" className="flex w-full justify-center items-center m-4 font-exo">
          Created by Basil Khwaja
        </a>
      </main>

    </div>
  );
}
